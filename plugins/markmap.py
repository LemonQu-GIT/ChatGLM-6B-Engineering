#coding:utf-8
from plugins.utils import *
import subprocess

def parse_markmap(input: str, history: list):
	prompt = f"我的问题是：“{input}”。你知道什么是markdown的源代码吧？是的话，你不用帮我生成思维导图，你只需要根据我的问题，生成一份关于我问题主题大纲的markdown源代码，我会用你的markdown代码来生成思维导图。在markdown格式中，# 表示中央主题， ## 表示主要主题，### 表示子主题，- 表示叶子节点。请参照以上格式进行回复。"
	with open("./src/assets/files/markdown_temp.md", "w", encoding='utf-8') as f:
		f.write('')
	alias = get_config()['markmap']['alias']
	log("Markmap service started", "EVENT")
	proc = subprocess.Popen(f'{alias} ./src/assets/files/markdown_temp.md -w',shell=True,stdout=subprocess.PIPE)
	for i in iter(proc.stdout.readline, 'b'): #type: ignore
		return_val = i.decode('utf-8')
		if "Listening at" in return_val:
			url = return_val.replace('Listening at ', '').strip()
			print(url)
		break
	payload = {
		"input": prompt,
		"history": history,
	}
	url = f"{get_config()['basic']['host']}:{get_config()['basic']['port']}/stream"
	response = requests.post(url, stream=True, json = payload)
	log("Woring on results", "EVENT")
	for chunk in response.iter_content(chunk_size=8192):
		resp = str(chunk.decode('utf-8', 'ignore')).replace('data: ', '').replace('```markdown', '').replace('```', '')
		if '以上' in resp:
			markdown = str(resp.split('以上')[0])
		else:
			markdown = str(resp)
		with open("./src/assets/files/markdown_temp.md", "w", encoding='utf-8') as f:
			f.write(markdown)
	proc.kill()

def if_trigger_markmap(word):
	triggers = get_config()['markmap']['trigger_words']
	for trigger in triggers:
		if trigger in word:
			return True
	else:
		return False

def run(prompt: str, history: list):
	if if_trigger_markmap(prompt):
		parse_markmap(prompt, history)