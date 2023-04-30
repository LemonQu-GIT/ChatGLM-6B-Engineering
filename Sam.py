import argparse
import os
import copy
from Segment_anything.utils.amg import remove_small_regions
from transformers import AutoModel, AutoTokenizer, AutoConfig
import numpy as np
import json
import openai
import torch
import torchvision
from PIL import Image, ImageDraw, ImageFont
import nltk

# Grounding DINO
import GroundingDINO.groundingdino.datasets.transforms as T
from GroundingDINO.groundingdino.models import build_model
from GroundingDINO.groundingdino.util import box_ops
from GroundingDINO.groundingdino.util.slconfig import SLConfig
from GroundingDINO.groundingdino.util.utils import clean_state_dict, get_phrases_from_posmap
import sys
# segment anything
# sys.path.append(r'./segment_anything')
from Segment_anything import build_sam, SamAutomaticMaskGenerator
from Segment_anything import SamPredictor
import cv2
import numpy as np
import matplotlib.pyplot as plt
# from segment_anything import build_sam, SamPredictor
# Tag2Text

sys.path.append(r'./Tag2Text')
from Tag2Text.models import tag2text
from Tag2Text import inference
import torchvision.transforms as TS
# BLIP
from transformers import BlipProcessor, BlipForConditionalGeneration
# ChatGPT or nltk is required when using captions
# import openai
# import nltk


def load_image(image_path):
    # load image
    image_pil = Image.open(image_path).convert("RGB")  # load image

    transform = T.Compose([
        T.RandomResize([800], max_size=1333),
        T.ToTensor(),
        T.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
    ])
    image, _ = transform(image_pil, None)  # 3, h, w
    return image_pil, image


# def generate_caption(raw_image, device):
#     # unconditional image captioning
#     if device == "cuda":
#         inputs = processor(raw_image, return_tensors="pt").to("cuda", torch.float16)
#     else:
#         inputs = processor(raw_image, return_tensors="pt")
#     out = blip_model.generate(**inputs)
#     caption = processor.decode(out[0], skip_special_tokens=True)
#     return caption


def generate_tags(caption, split=',', max_tokens=100, model="gpt-3.5-turbo"):
    lemma = nltk.wordnet.WordNetLemmatizer()
    if openai_key:
        prompt = [
            {
                'role': 'system',
                'content': 'Extract the unique nouns in the caption. Remove all the adjectives. ' + \
                           f'List the nouns in singular form. Split them by "{split} ". ' + \
                           f'Caption: {caption}.'
            }
        ]
        response = openai.ChatCompletion.create(model=model, messages=prompt, temperature=0.6, max_tokens=max_tokens)
        reply = response['choices'][0]['message']['content']
        # sometimes return with "noun: xxx, xxx, xxx"
        tags = reply.split(':')[-1].strip()
    else:
        nltk.download(['punkt', 'averaged_perceptron_tagger', 'wordnet'])
        tags_list = [word for (word, pos) in nltk.pos_tag(nltk.word_tokenize(caption)) if pos[0] == 'N']
        tags_lemma = [lemma.lemmatize(w) for w in tags_list]
        tags = ', '.join(map(str, tags_lemma))
    return tags


# global model_chatglm
tokenizer_chatglm = AutoTokenizer.from_pretrained("6b-int4", trust_remote_code=True)
model_chatglm = AutoModel.from_pretrained("6b-int4", trust_remote_code=True).half().cuda()
model_chatglm = model_chatglm.eval()


def check_caption(caption, pred_phrases, max_tokens=4096, model="gpt-3.5-turbo"):
    object_list = [obj.split('(')[0] for obj in pred_phrases]
    object_num = []
    for obj in set(object_list):
        object_num.append(f'{object_list.count(obj)} {obj}')
    object_num = ', '.join(object_num)
    print(f"Correct object number: {object_num}")

    if openai_key:
        # prompt = [
        #     {
        #         'role': 'system',
        #         'content': 'Revise the number in the caption if it is wrong. ' + \
        #                    f'Caption: {caption}. ' + \
        #                    f'True object number: {object_num}. ' + \
        #                    'Only give the revised caption: '
        #     }
        # ]
        prompt = 'Now your role is a system, and your responsibility is to revise the numbers in the Caption if it is wrong.' + f'Caption: {caption}. ' + f'True object number: {object_num}. ' + 'Only return the Caption: '

        response, _ = model_chatglm.chat(tokenizer_chatglm, prompt, None, max_length=max_tokens, top_p=0.8, temperature=0.6)
        # response = openai.ChatCompletion.create(model=model, messages=prompt, temperature=0.6, max_tokens=max_tokens)
        print('response为： ', response)
        # reply = response['choices'][0]['message']['content']
        # sometimes return with "Caption: xxx, xxx, xxx"
        # caption = reply.split(':')[-1].strip()
        caption = response.split(':')[-1].strip()
    return caption


def load_model(model_config_path, model_checkpoint_path, device):
    args = SLConfig.fromfile(model_config_path)
    args.device = device
    model = build_model(args)
    checkpoint = torch.load(model_checkpoint_path, map_location="cpu")
    load_res = model.load_state_dict(clean_state_dict(checkpoint["model"]), strict=False)
    print(load_res)
    _ = model.eval()
    return model


def get_grounding_output(model, image, caption, box_threshold, text_threshold, device="cpu"):
    caption = caption.lower()
    caption = caption.strip()
    if not caption.endswith("."):
        caption = caption + "."
    model = model.to(device)
    image = image.to(device)
    with torch.no_grad():
        outputs = model(image[None], captions=[caption])
    logits = outputs["pred_logits"].cpu().sigmoid()[0]  # (nq, 256)
    boxes = outputs["pred_boxes"].cpu()[0]  # (nq, 4)
    logits.shape[0]

    # filter output
    logits_filt = logits.clone()
    boxes_filt = boxes.clone()
    filt_mask = logits_filt.max(dim=1)[0] > box_threshold
    logits_filt = logits_filt[filt_mask]  # num_filt, 256
    boxes_filt = boxes_filt[filt_mask]  # num_filt, 4
    logits_filt.shape[0]

    # get phrase
    tokenlizer = model.tokenizer
    tokenized = tokenlizer(caption)
    # build pred
    pred_phrases = []
    scores = []
    for logit, box in zip(logits_filt, boxes_filt):
        pred_phrase = get_phrases_from_posmap(logit > text_threshold, tokenized, tokenlizer)
        pred_phrases.append(pred_phrase + f"({str(logit.max().item())[:4]})")
        scores.append(logit.max().item())

    return boxes_filt, torch.Tensor(scores), pred_phrases


def show_mask(mask, ax, random_color=False):
    if random_color:
        color = np.concatenate([np.random.random(3), np.array([0.6])], axis=0)
    else:
        color = np.array([30 / 255, 144 / 255, 255 / 255, 0.6])
    h, w = mask.shape[-2:]
    mask_image = mask.reshape(h, w, 1) * color.reshape(1, 1, -1)
    ax.imshow(mask_image)


def show_box(box, ax, label):
    x0, y0 = box[0], box[1]
    w, h = box[2] - box[0], box[3] - box[1]
    ax.add_patch(plt.Rectangle((x0, y0), w, h, edgecolor='green', facecolor=(0, 0, 0, 0), lw=2))
    ax.text(x0, y0, label)


def save_mask_data(output_dir, caption, mask_list, box_list, label_list):
    value = 0  # 0 for background

    mask_img = torch.zeros(mask_list.shape[-2:])
    for idx, mask in enumerate(mask_list):
        mask_img[mask.cpu().numpy()[0] == True] = value + idx + 1
    plt.figure(figsize=(10, 10))
    plt.imshow(mask_img.numpy())
    plt.axis('off')
    plt.savefig(os.path.join(output_dir, 'mask.jpg'), bbox_inches="tight", dpi=300, pad_inches=0.0)

    json_data = {'caption': caption, 'mask': [{'value': value, 'label': 'background'}]}
    for label, box in zip(label_list, box_list):
        value += 1
        name, logit = label.split('(')
        logit = logit[:-1]  # the last is ')'
        json_data['mask'].append({
            'value': value,
            'label': name,
            'logit': float(logit),
            'box': box.numpy().tolist(),
        })
    with open(os.path.join(output_dir, 'label.json'), 'w') as f:
        json.dump(json_data, f)


class SearchBase:
    def __init__(self) -> None:
        # 基础配置
        self.config_file = r'GroundingDINO/groundingdino/config/GroundingDINO_SwinT_OGC.py'  # change the path of the model config file
        self.tag2text_checkpoint = r'pth_data/tag2text_swin_14m.pth'  # change the path of the model
        self.grounded_checkpoint = r'pth_data/groundingdino_swint_ogc.pth'  # change the path of the model
        self.sam_checkpoint = r'pth_data/sam_vit_h_4b8939.pth'
        self.image_path = None
        self.split = ','
        self.openai_key = True
        self.openai_proxy = None
        self.output_dir = 'outputs'
        self.box_threshold = 0.25
        self.text_threshold = 0.2
        self.iou_threshold = 0.5
        self.device = 'cuda'
        # 函数调用参数
        self.image_pil = None
        self.image = None
        self.MatherPathofImage = None
        self.normalize = None
        self.transform = None
        self.specified_tags = 'None'
        self.GroundingDinoModel = None
        self.tag2text_model = None
        self.model_chatglm = None
        self.tokenizer_chatglm = None
        self.sam_model = None
        self.predictor = None
        self.boxes_filt = None
        self.scores = None
        self.pred_phrases = None
        self.caption = None
        self.text_prompt = None

    # Grounding Dino模型初始化
    def GroundingDinoModelInit(self):
        # make dir
        os.makedirs(self.output_dir, exist_ok=True)
        # load model
        model = load_model(self.config_file, self.grounded_checkpoint, device=self.device)
        return model

    # 图片装载器
    def ImageLoader(self, path2image):
        try:
            os.path.isfile(path2image)
        except IOError:
            print("请导入正确的路径并确认文件是否存在且具有读取权限!")
        else:
            # load image
            self.image_path = path2image
            self.image_pil, self.image = load_image(self.image_path)
            # return image_pil, image

    def Tag2TextInit(self):
        self.normalize = TS.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
        self.transform = TS.Compose([TS.Resize((384, 384)), TS.ToTensor(), self.normalize])
        # filter out attributes and action categories which are difficult to grounding
        delete_tag_index = []
        for i in range(3012, 3429):
            delete_tag_index.append(i)
        self.specified_tags = 'None'
        # load model
        tag2text_model = tag2text.tag2text_caption(pretrained=self.tag2text_checkpoint,
                                                   image_size=384,
                                                   vit='swin_b',
                                                   delete_tag_index=delete_tag_index)
        # threshold for tagging
        # we reduce the threshold to obtain more tags
        tag2text_model.threshold = 0.64
        tag2text_model.eval()
        tag2text_model = tag2text_model.to(self.device)
        return tag2text_model

    # 文件索引初始化
    # def LoaderYield(self):
    #     if not self.MatherPathofImage:
    #         print("文件初始化遍历路径生产器已禁用(调用此函数不会进行任何操作)")
    #     else:
    #         with open(r'D:\searchlist.txt') as f:
    #             files = []
    #             for item in os.scandir(self.MatherPathofImage):
    #                 # if item.is_dir():
    #                 #     dirs.append(item.path)
    #                 if item.is_file() and item[-4:] in ['.jpg', '.png', '.bmp']:
    #                     f.writelines(item)
    #                     files.append(item.path)

    def model_chatglm_load(self):
        # global model_chatglm
        self.tokenizer_chatglm = AutoTokenizer.from_pretrained("6b-int4", trust_remote_code=True)
        self.model_chatglm = AutoModel.from_pretrained("6b-int4", trust_remote_code=True).half().cuda()
        self.model_chatglm = self.model_chatglm.eval()
        return self.model_chatglm, self.tokenizer_chatglm

    def check_caption_GLM(self, caption, pred_phrases, max_tokens=4096):
        object_list = [obj.split('(')[0] for obj in pred_phrases]
        object_num = []
        for obj in set(object_list):
            object_num.append(f'{object_list.count(obj)} {obj}')
        object_num = ', '.join(object_num)
        print(f"Correct object number: {object_num}")

        if self.openai_key:
            prompt = '"prompt":Now your role is a system, and your responsibility is to revise the numbers in the Caption if it is wrong.' + f'Caption: {caption}. ' + f'True object number: {object_num}. ' + 'Only return the Caption: '
            response, _ = self.model_chatglm.chat(self.tokenizer_chatglm,
                                                  prompt,
                                                  None,
                                                  max_length=max_tokens,
                                                  top_p=0.8,
                                                  temperature=0.6)
            # response = openai.ChatCompletion.create(model=model, messages=prompt, temperature=0.6, max_tokens=max_tokens)
            print('response为： ', response)
            # reply = response['choices'][0]['message']['content']
            # sometimes return with "Caption: xxx, xxx, xxx"
            # caption = reply.split(':')[-1].strip()
            caption = response.split(':')[-1].strip()
        return caption

    def save_mask_data(self, output_dir, caption, mask_list, box_list, label_list):
        value = 0  # 0 for background

        mask_img = torch.zeros(mask_list.shape[-2:])
        for idx, mask in enumerate(mask_list):
            mask_img[mask.cpu().numpy()[0] == True] = value + idx + 1
        plt.figure(figsize=(10, 10))
        plt.imshow(mask_img.numpy())
        plt.axis('off')
        plt.savefig(os.path.join(output_dir, 'mask.jpg'), bbox_inches="tight", dpi=300, pad_inches=0.0)

        json_data = {'caption': caption, 'mask': [{'value': value, 'label': 'background'}]}
        for label, box in zip(label_list, box_list):
            value += 1
            name, logit = label.split('(')
            logit = logit[:-1]  # the last is ')'
            json_data['mask'].append({
                'value': value,
                'label': name,
                'logit': float(logit),
                'box': box.numpy().tolist(),
            })
        with open(os.path.join(output_dir, 'label.json'), 'w') as f:
            json.dump(json_data, f)

    def SAMLoader(self):
        self.sam_model = build_sam(checkpoint=self.sam_checkpoint).to(self.device)
        self.predictor = SamPredictor(self.sam_model)
        return self.predictor

    def SAMbaseonGroundingino(self):
        # initialize SAM
        image = cv2.imread(self.image_path)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        self.predictor.set_image(image)
        size = self.image_pil.size
        print('\n size: ', size)
        H, W = size[1], size[0]
        for i in range(self.boxes_filt.size(0)):
            self.boxes_filt[i] = self.boxes_filt[i] * torch.Tensor([W, H, W, H])
            self.boxes_filt[i][:2] -= self.boxes_filt[i][2:] / 2
            self.boxes_filt[i][2:] += self.boxes_filt[i][:2]

        self.boxes_filt = self.boxes_filt.cpu()
        # use NMS to handle overlapped boxes
        print(f"Before NMS: {self.boxes_filt.shape[0]} boxes")
        nms_idx = torchvision.ops.nms(self.boxes_filt, self.scores, self.iou_threshold).numpy().tolist()
        self.boxes_filt = self.boxes_filt[nms_idx]
        self.pred_phrases = [self.pred_phrases[idx] for idx in nms_idx]
        print(f"After NMS: {self.boxes_filt.shape[0]} boxes")
        # generate mask
        transformed_boxes = self.predictor.transform.apply_boxes_torch(self.boxes_filt, image.shape[:2]).to(self.device)
        masks, _, _ = self.predictor.predict_torch(
            point_coords=None,
            point_labels=None,
            boxes=transformed_boxes.to(self.device),
            multimask_output=False,
        )
        # remove the mask when area < area_thresh (in pixels)
        new_masks = []
        for mask in masks:
            # reshape to be used in remove_small_regions()
            mask = mask.cpu().numpy().squeeze()
            mask, _ = remove_small_regions(mask, 100, mode="holes")
            mask, _ = remove_small_regions(mask, 100, mode="islands")
            new_masks.append(torch.as_tensor(mask).unsqueeze(0))
        masks = torch.stack(new_masks, dim=0)
        # draw output image
        plt.figure(figsize=(10, 10))
        plt.imshow(image)
        for mask in masks:
            show_mask(mask.cpu().numpy(), plt.gca(), random_color=True)
        for box, label in zip(self.boxes_filt, self.pred_phrases):
            show_box(box.numpy(), plt.gca(), label)
        # plt.title('Tag2Text-Captioning: ' + self.caption + '\n\n' + 'Tag2Text-Tagging: ' + self.text_prompt + '\n')
        plt.axis('off')
        plt.savefig(os.path.join(self.output_dir, "automatic_label_output.jpg"), bbox_inches="tight", dpi=300, pad_inches=0.0)
        save_mask_data(self.output_dir, self.caption, masks, self.boxes_filt, self.pred_phrases)

    def InitAllModel(self):
        self.GroundingDinoModel = self.GroundingDinoModelInit()
        self.tag2text_model = self.Tag2TextInit()
        # self.model_chatglm_load()

    def ModelFree(self):
        self.GroundingDinoModel = None
        self.tag2text_model = None
        pass
    def SearcherInit(self, path2image):
        self.ImageLoader(path2image=path2image)
        raw_image = self.image_pil.resize((384, 384))
        raw_image = self.transform(raw_image).unsqueeze(0).to(self.device)
        res = inference.inference(raw_image, self.tag2text_model, self.specified_tags)
        print('res: ', res)
        # Currently ", " is better for detecting single tags
        # while ". " is a little worse in some case
        self.text_prompt = res[0].replace(' |', ',')
        self.caption = res[2]
        print('\n', f"Caption: {self.caption}")
        print(f"Tags: {self.text_prompt}", '\n')

        # run grounding dino model
        self.boxes_filt, self.scores, self.pred_phrases = get_grounding_output(self.GroundingDinoModel,
                                                                               self.image,
                                                                               self.text_prompt,
                                                                               self.box_threshold,
                                                                               self.text_threshold,
                                                                               device=self.device)
        # self.caption = self.check_caption_GLM(self.caption, self.pred_phrases)
        # print(f"Revise caption with number: {self.caption}", '\n\n')
        return self.caption


if __name__ == "__main__":

    parser = argparse.ArgumentParser("Grounded-Segment-Anything Demo", add_help=True)
    parser.add_argument("--config",
                        type=str,
                        default='GroundingDINO/groundingdino/config/GroundingDINO_SwinT_OGC.py',
                        required=False,
                        help="path to config file")
    parser.add_argument("--tag2text_checkpoint",
                        type=str,
                        default=r'pth_data\tag2text_swin_14m.pth',
                        required=False,
                        help="path to checkpoint file")
    parser.add_argument("--grounded_checkpoint",
                        type=str,
                        default='pth_data\groundingdino_swint_ogc.pth',
                        required=False,
                        help="path to checkpoint file")
    parser.add_argument("--sam_checkpoint",
                        type=str,
                        required=False,
                        default='pth_data\sam_vit_h_4b8939.pth',
                        help="pth_data\sam_vit_h_4b8939.pth")
    # assets\demo9.jpg
    parser.add_argument("--input_image", type=str, default=r'example\demo9.jpg', required=False, help="path to image file")
    parser.add_argument("--split", default=",", type=str, help="split for text prompt")
    parser.add_argument("--openai_key",
                        type=str,
                        default='',
                        help="key for chatgpt")
    parser.add_argument("--openai_proxy", default=None, type=str, help="proxy for chatgpt")
    parser.add_argument("--output_dir", "-o", type=str, default="outputs", required=False, help="output directory")

    parser.add_argument("--box_threshold", type=float, default=0.25, help="box threshold")
    parser.add_argument("--text_threshold", type=float, default=0.2, help="text threshold")
    parser.add_argument("--iou_threshold", type=float, default=0.5, help="iou threshold")

    parser.add_argument("--device", type=str, default="cuda", help="running on cpu only!, default=False")
    args = parser.parse_args(args=[])

    # cfg
    config_file = args.config  # change the path of the model config file
    tag2text_checkpoint = args.tag2text_checkpoint  # change the path of the model
    grounded_checkpoint = args.grounded_checkpoint  # change the path of the model
    sam_checkpoint = args.sam_checkpoint
    image_path = args.input_image
    split = args.split
    openai_key = args.openai_key
    openai_proxy = args.openai_proxy
    output_dir = args.output_dir
    box_threshold = args.box_threshold
    text_threshold = args.text_threshold
    iou_threshold = args.iou_threshold
    device = args.device

    # ChatGPT or nltk is required when using captions
    # openai.api_key = openai_key
    # if openai_proxy:
    # openai.proxy = {"http": openai_proxy, "https": openai_proxy}

    # make dir
    os.makedirs(output_dir, exist_ok=True)
    # load image
    image_pil, image = load_image(image_path)
    # load model
    model = load_model(config_file, grounded_checkpoint, device=device)

    # visualize raw image
    image_pil.save(os.path.join(output_dir, "raw_image.jpg"))
    # processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-large")
    # if device == "cuda":
    #     blip_model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-large",
    #                                                               torch_dtype=torch.float16).to("cuda")
    # else:
    #     blip_model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-large")

    # initialize Tag2Text
    normalize = TS.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    transform = TS.Compose([TS.Resize((384, 384)), TS.ToTensor(), normalize])

    # filter out attributes and action categories which are difficult to grounding
    delete_tag_index = []
    for i in range(3012, 3429):
        delete_tag_index.append(i)

    specified_tags = 'None'
    # load model
    tag2text_model = tag2text.tag2text_caption(pretrained=tag2text_checkpoint,
                                               image_size=384,
                                               vit='swin_b',
                                               delete_tag_index=delete_tag_index)
    # threshold for tagging
    # we reduce the threshold to obtain more tags
    tag2text_model.threshold = 0.64
    tag2text_model.eval()

    tag2text_model = tag2text_model.to(device)
    raw_image = image_pil.resize((384, 384))
    raw_image = transform(raw_image).unsqueeze(0).to(device)

    res = inference.inference(raw_image, tag2text_model, specified_tags)
    print('res: ', res)
    # Currently ", " is better for detecting single tags
    # while ". " is a little worse in some case
    text_prompt = res[0].replace(' |', ',')
    caption = res[2]

    print(f"Caption: {caption}")
    print(f"Tags: {text_prompt}")

    # run grounding dino model
    boxes_filt, scores, pred_phrases = get_grounding_output(model,
                                                            image,
                                                            text_prompt,
                                                            box_threshold,
                                                            text_threshold,
                                                            device=device)

    # initialize SAM
    sam_model = build_sam(checkpoint=sam_checkpoint).to(device)
    predictor = SamPredictor(sam_model)
    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    predictor.set_image(image)
    size = image_pil.size
    print('\n size: ', size)
    # size = image.size()
    H, W = size[1], size[0]
    for i in range(boxes_filt.size(0)):
        boxes_filt[i] = boxes_filt[i] * torch.Tensor([W, H, W, H])
        boxes_filt[i][:2] -= boxes_filt[i][2:] / 2
        boxes_filt[i][2:] += boxes_filt[i][:2]

    boxes_filt = boxes_filt.cpu()
    # use NMS to handle overlapped boxes
    print(f"Before NMS: {boxes_filt.shape[0]} boxes")
    nms_idx = torchvision.ops.nms(boxes_filt, scores, iou_threshold).numpy().tolist()
    boxes_filt = boxes_filt[nms_idx]
    pred_phrases = [pred_phrases[idx] for idx in nms_idx]
    print(f"After NMS: {boxes_filt.shape[0]} boxes")
    caption = check_caption(caption, pred_phrases)
    print(f"Revise caption with number: {caption}")
    # generate mask
    transformed_boxes = predictor.transform.apply_boxes_torch(boxes_filt, image.shape[:2]).to(device)
    masks, _, _ = predictor.predict_torch(
        point_coords=None,
        point_labels=None,
        boxes=transformed_boxes.to(device),
        multimask_output=False,
    )
    # remove the mask when area < area_thresh (in pixels)
    new_masks = []
    for mask in masks:
        # reshape to be used in remove_small_regions()
        mask = mask.cpu().numpy().squeeze()
        mask, _ = remove_small_regions(mask, 100, mode="holes")
        mask, _ = remove_small_regions(mask, 100, mode="islands")
        new_masks.append(torch.as_tensor(mask).unsqueeze(0))
    masks = torch.stack(new_masks, dim=0)
    # draw output image
    plt.figure(figsize=(10, 10))
    plt.imshow(image)
    for mask in masks:
        show_mask(mask.cpu().numpy(), plt.gca(), random_color=True)
    for box, label in zip(boxes_filt, pred_phrases):
        show_box(box.numpy(), plt.gca(), label)

    plt.title('Tag2Text-Captioning: ' + caption + '\n\n' + 'Tag2Text-Tagging: ' + text_prompt + '\n')
    plt.axis('off')
    plt.savefig(os.path.join(output_dir, "automatic_label_output.jpg"), bbox_inches="tight", dpi=300, pad_inches=0.0)

    save_mask_data(output_dir, caption, masks, boxes_filt, pred_phrases)
