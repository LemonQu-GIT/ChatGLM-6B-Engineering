from PIL import Image
from clip_interrogator import Config, Interrogator
import requests, json

global ci
ci = Interrogator(Config(clip_model_name="ViT-L-14/openai"))

def clip_image(filename):
    global ci
    image = Image.open(filename).convert('RGB')
    return ci.interrogate(image) # type: ignore

def clip_trans(word):
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
        return result["translateResult"][0][0]["tgt"]
