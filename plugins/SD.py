#coding:utf-8
from plugins.utils import *

def stable_diffusion(Pprompt,Nprompt, steps):
	url = str(get_config().get('SD').get('host'))+":"+str(get_config().get('SD').get('port'))
	payload = {
		"prompt": Pprompt,
		"steps": steps,
		"negative_prompt": Nprompt
	}
	response = requests.post(url=f'{url}/sdapi/v1/txt2img', json=payload)
	r = response.json()
	for i in r['images']:
		image = Image.open(io.BytesIO(base64.b64decode(i.split(",",1)[0])))
		png_payload = {
			"image": "data:image/png;base64," + i
		}
		response2 = requests.post(url=f'{url}/sdapi/v1/png-info', json=png_payload)
		pnginfo = PngImagePlugin.PngInfo()
		pnginfo.add_text("parameters", response2.json().get("info"))
		image.save('./src/assets/imgs/stable_diffusion.png', pnginfo=pnginfo)