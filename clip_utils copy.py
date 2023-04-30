from PIL import Image
from clip_interrogator import Config, Interrogator
import requests, json
import torch
from Fun_tool import SearchBase
global ci
ci = Interrogator(Config(clip_model_name="ViT-L-14/openai"))
# Config(caption_model='blip_image_captioning_large',clip_model_name="ViT-L-14/openai")
DEVICE = "cuda"
DEVICE_ID = "0"
CUDA_DEVICE = f"{DEVICE}:{DEVICE_ID}" if DEVICE_ID else DEVICE
def clip_image(filename):
    global ci
    image = Image.open(filename).convert('RGB')
    # ci = Interrogator(Config(caption_model_name='blip-large-local',clip_model_path="openaiclip_vit_large_patch14"))
    return ci.interrogate(image) # type: ignore

def torch_gc():
    if torch.cuda.is_available():
        with torch.cuda.device(CUDA_DEVICE):
            torch.cuda.empty_cache()
            torch.cuda.ipc_collect()

def clip_trans(word):
    image = Image.open(word).convert('RGB')
    ci = Interrogator(Config(caption_model_name='blip-large',clip_model_path="openaiclip_vit_large_patch14"))
    word = ci.interrogate(image)
    url = "http://fanyi.youdao.com/translate?smartresult=dict&smartresult=rule&smartresult=ugc&sessionFrom=null"
    key = {
        "type": "AUTO",
        "i": word,
        "doctype": "json",
        "version": "2.1",
        "keyfrom": "fanyi.web",
        "ue": "UTF-8",
        "action": "FY_BY_CLICKBUTTON",
        "typoResult": "true",
    }
    response = requests.post(url, data=key)
    if response.status_code == 200:
        list_trans = response.text
        result = json.loads(list_trans)
        ci = None
        torch_gc()
        return result["translateResult"][0][0]["tgt"]
    else :
        torch_gc()
        ci = None

def Tag2Text_trans(word):
    chatbot = SearchBase()
    # chatbot.model_chatglm_load()
    chatbot.InitAllModel()
    word = chatbot.SearcherInit(word)
    chatbot.ModelFree()
    chatbot.SAMLoader()
    chatbot.SAMbaseonGroundingino()
    url = "http://fanyi.youdao.com/translate?smartresult=dict&smartresult=rule&smartresult=ugc&sessionFrom=null"
    key = {
        "type": "AUTO",
        "i": word,
        "doctype": "json",
        "version": "2.1",
        "keyfrom": "fanyi.web",
        "ue": "UTF-8",
        "action": "FY_BY_CLICKBUTTON",
        "typoResult": "true",
    }
    response = requests.post(url, data=key)
    if response.status_code == 200:
        list_trans = response.text
        result = json.loads(list_trans)
        chatbot = None
        torch_gc()
        return result["translateResult"][0][0]["tgt"]
    else :
        torch_gc()
        chatbot = None
