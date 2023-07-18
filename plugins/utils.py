#coding:utf-8
import json, requests, base64, io, re, time, datetime, os, sys
from urllib.parse import quote
from PIL import Image, PngImagePlugin
from rich.console import Console
console = Console()

def get_config():
	with open("./plugins/config.json", encoding='utf-8') as f:
		return json.load(f)

def plugin_status():
	enable_dict = {}
	try:
		for i in range(get_config()['plugins']['count']):
			plugin_list = get_config()['plugins'][str(i)]
			enable_dict.update({plugin_list['name']: plugin_list['enable']})
		return enable_dict
	except:
		log("Plugin count failed", "ERROR")
		return {}

def log(event:str, type:str):
	back_frame = sys._getframe().f_back
	if back_frame is not None:
		back_filename = os.path.basename(back_frame.f_code.co_filename)
		back_funcname = back_frame.f_code.co_name
		back_lineno = back_frame.f_lineno
	else:
		back_filename = "Unknown"
		back_funcname = "Unknown"
		back_lineno = "Unknown"
	now = datetime.datetime.now()
	time = now.strftime("%Y-%m-%d %H:%M:%S")
	logger = f"[{time}] <{back_filename}:{back_lineno}> <{back_funcname}()> {type}: {event}"
	if type.lower() == "info":
		style = "green"
	elif type.lower() == "error":
		style = "red"
	elif type.lower() == "critical":
		style = "bold red"
	elif type.lower() == "event":
		style = "#ffab70"
	else:
		style = ""
	console.print(logger, style = style)
	with open('latest.log','a', encoding='utf-8') as f:
		f.write(f'{logger}\n')

def change_cfg(weather: bool, date: bool, web: bool, markmap: bool, files: bool, sd: bool):
	with open('./plugins/config.json', 'r', encoding='utf-8') as f:
		result = f.read()
	results=json.loads(result)
	results['plugins']['0']['enable'] = weather
	results['plugins']['1']['enable'] = date
	results['plugins']['2']['enable'] = web
	results['plugins']['3']['enable'] = markmap
	results['plugins']['4']['enable'] = files
	results['plugins']['5']['enable'] = sd
	with open('./plugins/config.json', 'w', encoding='utf-8') as new_f:
		new_f.write(json.dumps(results, ensure_ascii=False, indent=1))

def chatglm_json(prompt, history):
	try:
		url = str(get_config().get('basic').get('host'))+":"+str(get_config().get('basic').get('port'))+ "/default"
		payload = {
			"prompt": prompt,
			"history": history
		}
		response = requests.post(url, json=payload)
		json_resp_raw = response.json()
		json_resp_raw_list = json.dumps(json_resp_raw)
		return json_resp_raw_list
	except:
		log("Default ChatGLM-6B request failed", "CRITICAL")
		return "None"


def test_if_zhcn(string):
	for ch in string:
		if u'\u4e00' <= ch <= u'\u9fff':
			return True
	return False

def translate(word):
	if test_if_zhcn(word):
		url = 'http://fanyi.youdao.com/translate?smartresult=dict&smartresult=rule&smartresult=ugc&sessionFrom=null'
		key = {
			'type': "AUTO",
			'i': word,
			"doctype": "json",
			"version": "2.1",
			"keyfrom": "fanyi.web",
			"ue": "UTF-8",
			"action": "FY_BY_CLICKBUTTON",
			"typoResult": "true"
		}
		response = requests.post(url, data=key)
		if response.status_code == 200:
			list_trans = response.text
			result = json.loads(list_trans)
			return result['translateResult'][0][0]['tgt']
	else:
		return word

def validate_config():
	log(f'Validating config', "INFO")
	if os.environ.get('VUE_APP_API') is not None or get_config()['API_host'] is not None:
		if  os.environ.get('VUE_APP_API') is not None:
			api_host = os.environ.get('VUE_APP_API')
		if get_config()['API_host'] is not None:
			api_host = get_config()['API_host']
		log(f'API host exists, Host: {api_host}', "INFO")
		if os.path.exists('./plugins/config.json'):
			log(f'config.json exists', "INFO")
			try:
				chatglm_port = get_config()['basic']['port']
				if 1 <= chatglm_port <= 65535:
					chatglm_host = get_config()['basic']['host']
				else:
					log('Incorrect API port.', "CRITICAL")
					os._exit(0)
				chatglm_url = f"{chatglm_host}:{chatglm_port}"
				log(f'API url: {chatglm_url}', "INFO")
				try:
					log(f'Pinging API', "INFO")
					response = requests.post(chatglm_url+"/ping")
					log(f'API use {response.elapsed.total_seconds()} seconds to response, response: {response.text}', "INFO")
				except:
					log('Error while API giving response. Program exited.', "CRITICAL")
					os._exit(0)
				try:
					log(f'Pinging https://cn.bing.com', "INFO")
					response = requests.get("https://cn.bing.com")
					log(f'Using {response.elapsed.total_seconds()} seconds to get https://cn.bing.com', "INFO")
				except:
					log('Error while browsering Internet. Functionality might be limited.', "ERROR")
				log("Validation Passed.", "INFO")
			except:
				log('Failed to load config. Broken content.', "CRITICAL")
				os._exit(0)
		else:
			log('config.json not found. Program exited', "CRITICAL")
			os._exit(0)
	else:
		log('VUE_APP_API not found. Program exited', "CRITICAL")
		os._exit(0)