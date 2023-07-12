#coding:utf-8
import json, uvicorn, requests, os, asyncio
from fastapi import FastAPI, Response, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from plugins import *


app = FastAPI()
origins = ["*"]
app.add_middleware(
	CORSMiddleware,
	allow_origins = origins,
	allow_credentials = True,
	allow_methods = ["*"],
	allow_headers = ["*"]
)

latest_filename = ""
latest_filesize = ""
history = []
chat_prompt = ""
chat_response=  ""
if os.environ.get('VUE_APP_API') is not None:
	host = os.environ.get('VUE_APP_API')
if get_config()['API_host'] is not None:
	host = get_config()['API_host']

print(host)
@app.get("/api/repeat")
def repeat():
	try:
		global history, chat_response
		log(f'Chat message: {repr(chat_response)} requests to repeat', "EVENT")
		request = chatglm_json(str(chat_response), history=history)
		request_list = json.loads(request)
		response = request_list.get('response')
		log(f'Chat message: {repr(chat_response)} repeats finished. Response: {repr(response)}', "INFO")
		return Response(f"{response}")
	except:
		log('Error while repeating chat message', "ERROR")
		return Response("<font color=#e54240>Something went wrong...</font>")

@app.get("/api/chat")
async def chat_stream(prompt: str):
	global history, chat_response, latest_filename, latest_filesize, chat_prompt
	async def chat(prompt: str):
		global history, chat_response, latest_filename, latest_filesize, chat_prompt
		add_prompt = ''
		prefix = ''
		suffix = ''
		pl_status = plugin_status()
		enable_weather = pl_status['weather']
		enable_date = pl_status['date']
		enable_web = pl_status['web']
		enable_markmap = pl_status['markmap']
		enable_files = pl_status['files']
		#enable_SD = pl_status['SD']

		if enable_weather:
			log('Calling weather plugin', 'EVENT')
			weather_resp = weather.run(prompt)
			if weather_resp != None:
				add_prompt += weather_resp['add']
				prefix += weather_resp['prefix']
				suffix += weather_resp['suffix']
				log(f"Weather plugin finished, added: {add_prompt}", "EVENT")
    
		if enable_date:
			log('Calling date plugin', 'EVENT')
			date_resp = date.run(prompt)
			if date_resp != None:
				add_prompt += date_resp['add']
				prefix += date_resp['prefix']
				suffix += date_resp['suffix']
				log(f"Date plugin finished, added: {add_prompt}", "EVENT")
    
		if enable_web:
			log('Calling web plugin', 'EVENT')
			web_resp = web.run(prompt)
			if web_resp != None:
				add_prompt += web_resp['add']
				prefix += web_resp['prefix']
				suffix += web_resp['suffix']
				log(f"Web plugin finished", "EVENT")
    
		if enable_files:
			log('Calling files plugin', 'EVENT')
			if not latest_filename == "":
				files_resp = upload.run(latest_filename)
				log(f"Input file suffix: {suffix}", "INFO")
				if files_resp != None:
					add_prompt += files_resp['add']
					prefix += files_resp['prefix']
					suffix += files_resp['suffix']
					log(f"Files plugin finished", "EVENT")
          
		if enable_markmap:
			log('Calling markmap plugin', 'EVENT')
			if markmap.if_trigger_markmap(prompt):
				input = f"我的问题是：“{prompt}”。你知道什么是markdown的源代码吧？是的话，你不用帮我生成思维导图，你只需要根据我的问题，生成一份关于我问题主题大纲的markdown源代码，我会用你的markdown代码来生成思维导图。在markdown格式中，# 表示中央主题， ## 表示主要主题，### 表示子主题，- 表示叶子节点。你不需要用代码块（```）将markdown括起来，你可以直接回复内容。请参照以上格式进行回复。"
				with open("./plugins/markdown_temp.md", "w", encoding='utf-8') as f:
					f.write('')
				alias = get_config()['markmap']['alias']
				proc = subprocess.Popen(f'{alias} ./plugins/markdown_temp.md -w',shell=True,stdout=subprocess.PIPE)
				for i in iter(proc.stdout.readline, 'b'): #type: ignore
					return_val = i.decode('utf-8')
					if "Listening at" in return_val:
						url = return_val.replace('Listening at ', '').strip()
						log(f"Markmap server started. URL: {url}", "EVENT")
					break
				pre_yield = f'<iframe\nheight="450"\nwidth="800"\nsrc="{url}"\nframeborder="0"\nallowfullscreen\n>\n</iframe>' #type: ignore
				payload = {
					"prompt": input,
					"history": history,
					"prefix": f"\n{pre_yield}"
				}
				url = f"{get_config()['basic']['host']}:{get_config()['basic']['port']}/stream"
				response = requests.post(url, stream=True, json = payload)
				for chunk in response.iter_content(chunk_size=8192):
					await asyncio.sleep(0.1)
					reloads = chunk.decode('utf-8', 'ignore')
					yield reloads
					resp = str(chunk.decode('utf-8', 'ignore')).replace('data: ', '').replace('```markdown', '').replace('```', '')
					markdown = ''
					try:
						markdown = str(resp.split('</iframe>')[1])
					except:
						markdown = markdown
					if '以上' in markdown:
						markdown = str(markdown.split('以上')[0])
					with open("./plugins/markdown_temp.md", "w", encoding='utf-8') as f:
						f.write(markdown)
				proc.kill()
				return

		if add_prompt == "" and suffix == "" and prefix == "":
			ask_prompt = prompt 
		else:
			ask_prompt = f"已知：'''{add_prompt}'''，我的问题是：{prompt}，请根据我给的信息及我的问题及你的思考给出回复"
		log(f"Chat prompt: {repr(ask_prompt)}", "INFO")
		payload = {
			"prompt": ask_prompt,
			"history": history,
			"prefix": prefix,
			"suffix": suffix
		}
		url = f"{get_config()['basic']['host']}:{get_config()['basic']['port']}/stream"
		response = requests.post(url, stream=True, json = payload)
		resp = ""
		for chunk in response.iter_content(chunk_size=1024):
			await asyncio.sleep(0.1)
			resp = chunk.decode('utf-8', 'ignore')
			yield resp
		chat_response = resp.replace("data: ", "")
		history.append([ask_prompt.strip(), chat_response.strip()])
		if len(history) > 10:
			history.pop(0)
		log(f"Chat history: {repr(history)}. Response: {repr(chat_response)}", "INFO")
		return
	return StreamingResponse(chat(prompt), media_type="text/event-stream")

@app.post("/api/stop")
def stop():
	log('User Interrupt', "CRITICAL")
	return Response("User Interrupt")

@app.post("/api/delete")
def delete():
	global chat_response, latest_filename, history
	chat_response = []
	latest_filename = ""
	history = []
	log('User history deleted', "EVENT")

@app.get("/api/sdimg")
def image():
	log('Get stable diffusion image', "EVENT")
	data = open('./plugins/stable_diffusion.png', "rb")
	return StreamingResponse(data, media_type="image/png")

@app.post("/api/upload")
async def upload_file(file: UploadFile = File(...)):
	contents = await file.read()
	#folder = os.getcwd()
	with open("./plugins/uploads/"+str(file.filename), "wb") as f:
		f.write(contents)
	global latest_filename, latest_filesize
	latest_filename = str(file.filename)
	latest_filesize = file.size
	if latest_filesize < 1024: # type:ignore
		latest_filesize = round(latest_filesize,2),'Byte' # type:ignore
	else: 
		KBX = latest_filesize/1024 # type:ignore
		if KBX < 1024:
			latest_filesize = round(KBX,2),'KB'
		else:
			MBX = KBX /1024
			if MBX < 1024:
				latest_filesize = round(MBX,2),'MB'
			else:
				latest_filesize = round(MBX/1024),'GB'
	latest_filesize = str(latest_filesize[0]) +" "+ str(latest_filesize[1])
	log(f"Uploaded files, filename: {latest_filename}, filesize: {latest_filesize}", "EVENT")

@app.get("/api/title")
def title():
	global chat_response, chat_prompt, history
	request = chatglm_json(f"我的问题是：“{chat_prompt}”，请对我发送的内容进行概括，8个字以内，请直接回复概括内容，不需要回复其他内容", history)
	request_list = json.loads(request)
	title_text = str(request_list.get('response'))
	title_text = title_text.strip().replace("概括内容","").replace("概括文字","").replace("概括","").replace("：","").replace(":","").removesuffix("。").removesuffix(".").removesuffix("，").removesuffix(",")
	log(f"Generate title complete, title: {title_text}", "INFO")
	return Response(title_text)

@app.get("/api/renderfile")
def render_file(filename:str, filesize:str, filetime:str, filetype: str):
	if filetype == "pdf":
		svg = f'''<?xml version="1.0" encoding="UTF-8"?>
			<svg id="a" data-name="Path" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 655.1 224.1">
			<rect x="1.5" y="1.5" width="652.1" height="221.1" rx="17.2" ry="17.2" style="fill: #f2f2f2; stroke: #666; stroke-miterlimit: 10; stroke-width: 3px;"/>
			<g>
				<path d="m57,77.3c5.4,0,10.8,0,16.2,0,6.7,0,13.3,0,20,0,3.3,0,5.8,1.2,7.8,3.7,3.3,3.8,6.7,7.6,10,11.4,2.5,2.9,5,5.9,7.5,8.8,2.4,2.7,4.9,5.3,7,8.2.7,1.1,1,2.2,1.1,3.6.7,8.9,0,17.9.3,26.8,0,.8.3,1.1,1.1,1.1,1.7,0,3.3-.1,5,.3,3,.8,4.6,2.7,5.3,5.6.4,1.9.2,3.8.1,5.6,0,4.3.2,8.6-.2,12.9-.3,3.8-3,6.3-6.9,6.5-.9,0-1.9,0-2.8,0-1.3-.1-1.7.3-1.7,1.6,0,2.8,0,5.5,0,8.3,0,2.8-.7,5.5-3,7.4-1.8,1.6-3.8,2.5-6.4,2.5-5.9-.1-11.8,0-17.7,0-17.6,0-35.2,0-52.9,0-3.2,0-6-.7-8.4-2.8-1.6-1.5-2.8-3.3-3.1-5.6-.8-7.2-.3-14.4-.3-21.5,0-24.8,0-49.6,0-74.4,0-2.2.2-4.1,1.5-6,1.8-2.6,4.3-4,7.5-4,4.3,0,8.7,0,13,0h0Zm39.7,63.5c8.2,0,16.4,0,24.5,0,1,0,1.4-.2,1.4-1.3,0-7.6,0-15.2,0-22.9,0-1.1-.3-1.3-1.4-1.3-6.4,0-12.9,0-19.3,0-2.7,0-5-.6-7.1-2.2-2.2-1.7-3.7-3.8-3.8-6.7,0-7.9,0-15.8,0-23.6,0-1.2-.4-1.4-1.5-1.4-7.8,0-15.6,0-23.4,0-7.3,0-14.6,0-21.8,0-1,0-2,.3-2.9,1-1.6,1.2-2,2.7-1.9,4.7,0,30.9,0,61.8,0,92.8,0,.3,0,.5,0,.8-.4,2.4.8,4.1,2.6,5.5,1.5,1.2,3.2,1.2,5,1.2,22.9,0,45.8,0,68.7,0,.4,0,.8,0,1.2,0,3.5.1,5.7-2.6,5.6-5.6,0-2.8,0-5.6,0-8.5,0-1.2-.3-1.6-1.6-1.6-15.7,0-31.4,0-47,0-1.2,0-2.4.1-3.6-.2-1.2-.3-2.4-.9-3.2-1.8-1.4-1.6-2.1-3.6-2.1-5.9.1-5.1,0-10.3,0-15.5,0-1.2-.2-2.3.4-3.4,1.5-2.9,3.8-4.4,7.1-4.4,8,0,16,0,24,0Zm24.8-30c-2-1.1-2.8-3.2-4.3-4.7-1.4-1.5-2.8-3.1-4.1-4.8-2.2-2.8-4.6-5.5-6.9-8.2-.5-.5-.5-1.4-1.2-1.7-1.4-.8-2.2-2.1-3.1-3.2-1.7-2-3.3-4-5.2-5.9-.3-.3-.6-.8-1.1-.6-.6.2-.3.8-.3,1.2,0,4,0,8.1,0,12.1,0,3.6,0,7.2,0,10.8,0,2.4,2.6,5.3,5.3,5.2,6.6-.1,13.2,0,19.8,0,.3,0,.6,0,1.1-.3Zm-25.3,44.7c0,2,0,4,0,6.1,0,.7.2,1,1,1,2.6-.1,5.3.2,7.9-.2,2.1-.3,3.5-1.4,4-3.5.5-1.8.4-3.6.2-5.3-.2-2.1-1.4-4.1-3.5-4.7-2.9-.8-5.9-.4-8.9-.5-.8,0-.7.6-.7,1,0,2,0,4,0,6.1Zm-14.6,0h0c0,2,0,4.1,0,6.1,0,1,.5,1.2,1.3,1.1.8,0,1.9.4,1.9-1.1,0-.8,0-1.7,0-2.5,0-1,.2-1.4,1.3-1.4,1.5,0,3,0,4.6,0,.7,0,1.4-.1,2-.6,1.6-1.4,2.2-3.9,1.5-5.7-.8-2.1-2.7-2.8-4.7-2.9-2.2-.1-4.4,0-6.6,0-.9,0-1.2.2-1.2,1.1,0,2,0,4,0,5.9Zm37.1-1.3c-1.2,0-2.3,0-3.5,0-.6,0-.8-.2-.8-.8,0-1.4.9-2.2,2.8-2.3,1.6,0,3.3,0,5,0,1.1,0,.9-.7.8-1.2,0-.6.4-1.4-.8-1.4-2,0-3.9-.1-5.9.1-3.5.5-4.8,1.9-4.9,5.4,0,2.6,0,5.1,0,7.7,0,.9.4,1.2,1.2,1,.8-.1,2,.5,1.9-1.1,0-.9,0-1.8,0-2.8,0-2.3-.3-2,2-2,1.9,0,3.8,0,5.6,0,1.2,0,.9-.8.9-1.5,0-.7,0-1.2-.9-1.2-1.1,0-2.2,0-3.3,0Z" style="fill: #cc2525;"/>
				<path d="m95.3,83c0-.4-.3-1,.3-1.2.5-.2.8.3,1.1.6,1.9,1.9,3.5,3.9,5.2,5.9,1,1.1,1.8,2.4,3.1,3.2.6.3.7,1.2,1.2,1.7,2.4,2.7,4.8,5.3,6.9,8.2,1.3,1.7,2.7,3.3,4.1,4.8,1.5,1.5,2.2,3.6,4.3,4.7-.5.4-.8.3-1.1.3-6.6,0-13.2-.1-19.8,0-2.8,0-5.4-2.8-5.3-5.2,0-3.6,0-7.2,0-10.8,0-4,0-8.1,0-12.1Z" style="fill: #ffe1e1;"/>
				<path d="m122.6,173.4c0,2.8,0,5.6,0,8.5,0,3-2.1,5.7-5.6,5.6-.4,0-.8,0-1.2,0-22.9,0-45.8,0-68.7,0-1.8,0-3.5,0-5-1.2-1.8-1.4-3-3.1-2.6-5.5,0-.3,0-.5,0-.8,0-30.9,0-61.8,0-92.7,0-2,.4-3.5,1.9-4.7.9-.7,1.9-1,2.9-1,7.3,0,14.6,0,21.8,0,7.8,0,15.6,0,23.4,0,1.1,0,1.5.2,1.5,1.4,0,7.9,0,15.8,0,23.6,0,2.9,1.5,5,3.8,6.7,2.1,1.6,4.5,2.2,7.1,2.2,6.4,0,12.9,0,19.3,0,1,0,1.4.3,1.4,1.3,0,7.6,0,15.2,0,22.9,0,1.1-.4,1.3-1.4,1.3-8.2,0-16.4,0-24.5,0s-16,0-24,0c-3.3,0-5.6,1.5-7.1,4.4-.6,1.1-.4,2.2-.4,3.4,0,5.2.1,10.3,0,15.5,0,2.3.7,4.2,2.1,5.9.8.9,1.9,1.4,3.2,1.8,1.2.3,2.4.2,3.6.2,15.7,0,31.4,0,47,0,1.2,0,1.6.4,1.6,1.6Z" style="fill: #ffe1e1;"/>
				<path d="m96.2,155.6c0-2,0-4,0-6.1,0-.5-.1-1,.7-1,3,0,5.9-.3,8.9.5,2.1.6,3.3,2.6,3.5,4.7.1,1.8.2,3.6-.2,5.3-.5,2-1.8,3.1-4,3.5-2.6.4-5.3,0-7.9.2-.8,0-1-.3-1-1,0-2,0-4,0-6.1Zm3.1,0c0,.3,0,.6,0,.9,0,1.1-.5,2.6.2,3.3.8.7,2.3.1,3.5.2,1.4.1,2.2-.9,2.6-1.8.6-1.5.6-3.2,0-4.8-.4-1.3-1.5-2.1-2.9-2.3-.9,0-1.8,0-2.7,0-.6,0-.9.2-.8.9,0,1.2,0,2.5,0,3.7Z" style="fill: #ffe1e1;"/>
				<path d="m81.5,155.5c0-2,0-4,0-5.9,0-.9.3-1.1,1.2-1.1,2.2,0,4.4,0,6.6,0,2.1.1,3.9.8,4.7,2.9.7,1.8,0,4.3-1.5,5.7-.5.5-1.2.6-2,.6-1.5,0-3,0-4.6,0-1.1,0-1.4.4-1.3,1.4,0,.8,0,1.7,0,2.5,0,1.5-1.1,1-1.9,1.1-.8,0-1.3,0-1.3-1.1,0-2,0-4.1,0-6.1h0Zm5.9-4.4c-.5,0-1.1,0-1.6,0-.8,0-1.2.2-1.2,1.1,0,3,0,3,3,3,.4,0,.7,0,1.1,0,1.7,0,2.1-.5,2.1-2.3,0-1.4-.5-1.8-2.2-1.8-.4,0-.8,0-1.2,0Z" style="fill: #ffe1e1;"/>
				<path d="m118.7,154.3c1.1,0,2.2,0,3.3,0,1,0,1,.5.9,1.2,0,.6.3,1.5-.9,1.5-1.9,0-3.8,0-5.6,0-2.3,0-1.9-.3-2,2,0,.9,0,1.8,0,2.8,0,1.6-1.1.9-1.9,1.1-.8.1-1.2,0-1.2-1,0-2.6,0-5.1,0-7.7,0-3.5,1.4-4.9,4.9-5.4,2-.3,3.9,0,5.9-.1,1.2,0,.7.8.8,1.4,0,.6.2,1.3-.8,1.2-1.7,0-3.3,0-5,0-1.9.1-2.8.9-2.8,2.3,0,.6.2.8.8.8,1.2,0,2.3,0,3.5,0Z" style="fill: #ffe1e1;"/>
				<path d="m99.3,155.6c0-1.2,0-2.5,0-3.7,0-.6.2-.9.8-.9.9,0,1.8,0,2.7,0,1.4.1,2.5,1,2.9,2.3.5,1.6.6,3.3,0,4.8-.4.9-1.2,1.9-2.6,1.8-1.2,0-2.7.5-3.5-.2-.7-.6-.1-2.2-.2-3.3,0-.3,0-.6,0-.9Z" style="fill: #cc2525;"/>
				<path d="m87.4,151.1c.4,0,.8,0,1.2,0,1.7,0,2.1.4,2.2,1.8,0,1.8-.4,2.2-2.1,2.3-.4,0-.7,0-1.1,0-3,0-3,0-3-3,0-.9.3-1.2,1.2-1.1.5,0,1.1,0,1.6,0Z" style="fill: #cc2525;"/>
			</g>
			<text transform="translate(25.4 49.9) scale(1 1)" style="fill: #333; font-family: MicrosoftYaHeiUILight, &apos;Microsoft YaHei UI Light&apos;; font-size: 30.1px;"><tspan x="0" y="0">上传的文件</tspan></text>
			<text transform="translate(175.9 112.7) scale(1 1)" style="fill: #333; font-family: MicrosoftYaHeiUILight, &apos;Microsoft YaHei UI Light&apos;; font-size: 30.1px;"><tspan x="0" y="0">{filename}</tspan></text>
			<text transform="translate(176.7 153.6) scale(1 1)" style="fill: #4d4d4d; font-family: MicrosoftYaHeiUILight, &apos;Microsoft YaHei UI Light&apos;; font-size: 20.5px;"><tspan x="0" y="0">{filetime}</tspan></text>
			<text transform="translate(176.7 177.7) scale(1 1)" style="fill: #666; font-family: MicrosoftYaHeiUILight, &apos;Microsoft YaHei UI Light&apos;; font-size: 20.5px;"><tspan x="0" y="0">{filesize}</tspan></text>
			</svg>'''
	elif filetype == "code":
		svg = f'''<?xml version="1.0" encoding="UTF-8"?>
			<svg id="a" data-name="Path" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 655.1 224.1">
			<rect x="1.5" y="1.5" width="652.1" height="221.1" rx="17.2" ry="17.2" style="fill: #f2f2f2; stroke: #666; stroke-miterlimit: 10; stroke-width: 3px;"/>
			<path d="m139,152.4c0-1.9.3-3.8-.1-5.6-.6-2.9-2.2-4.8-5.2-5.6-1.7-.5-3.4-.3-5-.3-.8,0-1.1-.3-1.1-1.1-.2-8.9.5-17.9-.3-26.8-.1-1.4-.4-2.5-1.1-3.6-2.1-3-4.6-5.5-7-8.2-2.5-2.9-5-5.9-7.5-8.8-3.3-3.8-6.7-7.6-10-11.4-2.1-2.4-4.5-3.7-7.9-3.6-6.7.1-13.3,0-20,0h-16.2c-4.3,0-8.7,0-13,0-3.2,0-5.6,1.5-7.5,4-1.3,1.8-1.5,3.8-1.5,6,0,24.8,0,49.6,0,74.4,0,7.2-.5,14.4.3,21.5.3,2.4,1.5,4.1,3.1,5.6,2.3,2.1,5.1,2.8,8.4,2.8,17.6-.1,35.2,0,52.9,0s11.8,0,17.7,0c2.5,0,4.5-.9,6.4-2.5,2.3-2,2.9-4.6,3-7.4,0-2.8,0-5.5,0-8.3,0-1.3.4-1.7,1.7-1.6.9,0,1.9,0,2.8,0,3.9-.2,6.6-2.7,6.9-6.5.4-4.3,0-8.6.2-12.9Zm-42.8-70.6c.5-.2.8.3,1.1.6,1.9,1.9,3.5,3.9,5.2,5.9,1,1.1,1.8,2.4,3.1,3.2.6.3.7,1.2,1.2,1.7,2.4,2.7,4.8,5.3,6.9,8.2,1.3,1.7,2.7,3.3,4.1,4.8,1.5,1.5,2.2,3.6,4.3,4.7-.5.4-.8.3-1.1.3-6.6,0-13.2-.1-19.8,0-2.8,0-5.4-2.8-5.3-5.2,0-3.6,0-7.2,0-10.8s0-8.1,0-12.1c0-.4-.3-1,.3-1.2Zm27,100c0,3-2.1,5.7-5.6,5.6-.4,0-.8,0-1.2,0-22.9,0-45.8,0-68.7,0-1.8,0-3.5,0-5-1.2-1.8-1.4-3-3.1-2.6-5.5,0-.3,0-.5,0-.8,0-30.9,0-61.8,0-92.8,0-2,.4-3.5,2-4.7.9-.7,1.9-1,2.9-1,7.3,0,14.6,0,21.8,0,7.8,0,15.6,0,23.4,0,1.2,0,1.5.2,1.5,1.4,0,7.9,0,15.8,0,23.7,0,2.9,1.5,5,3.8,6.7,2.1,1.6,4.5,2.2,7.1,2.2,6.4,0,12.9,0,19.3,0,1,0,1.4.3,1.4,1.3,0,7.6,0,15.2,0,22.9,0,1.1-.3,1.3-1.4,1.3-8.2,0-16.3,0-24.5,0s-16,0-24,0c-3.3,0-5.6,1.5-7.1,4.4-.6,1.1-.4,2.2-.4,3.4,0,5.2.1,10.3,0,15.5,0,2.3.7,4.2,2.1,5.8.8.9,1.9,1.4,3.2,1.8,1.2.3,2.4.2,3.6.2,15.7,0,31.4,0,47,0,1.2,0,1.6.3,1.6,1.6,0,2.8,0,5.6,0,8.4Z" style="fill: #29abe2;"/>
			<path d="m95.9,83c0-.4-.3-1,.3-1.2.5-.2.8.3,1.1.6,1.9,1.9,3.5,3.9,5.2,5.9,1,1.1,1.8,2.4,3.1,3.2.6.3.7,1.2,1.2,1.7,2.4,2.7,4.8,5.3,6.9,8.2,1.3,1.7,2.7,3.3,4.1,4.8,1.5,1.5,2.2,3.6,4.3,4.7-.5.4-.8.3-1.1.3-6.6,0-13.2-.1-19.8,0-2.8,0-5.4-2.8-5.3-5.2,0-3.6,0-7.2,0-10.8,0-4,0-8.1,0-12.1Z" style="fill: #e6e6e6;"/>
			<path d="m123.2,173.4c0,2.8,0,5.6,0,8.5,0,3-2.1,5.7-5.6,5.6-.4,0-.8,0-1.2,0-22.9,0-45.8,0-68.7,0-1.8,0-3.5,0-5-1.2-1.8-1.4-3-3.1-2.6-5.5,0-.3,0-.5,0-.8,0-30.9,0-61.8,0-92.7,0-2,.4-3.5,1.9-4.7.9-.7,1.9-1,2.9-1,7.3,0,14.6,0,21.8,0,7.8,0,15.6,0,23.4,0,1.1,0,1.5.2,1.5,1.4,0,7.9,0,15.8,0,23.6,0,2.9,1.5,5,3.8,6.7,2.1,1.6,4.5,2.2,7.1,2.2,6.4,0,12.9,0,19.3,0,1,0,1.4.3,1.4,1.3,0,7.6,0,15.2,0,22.9,0,1.1-.4,1.3-1.4,1.3-8.2,0-16.4,0-24.5,0s-16,0-24,0c-3.3,0-5.6,1.5-7.1,4.4-.6,1.1-.4,2.2-.4,3.4,0,5.2.1,10.3,0,15.5,0,2.3.7,4.2,2.1,5.9.8.9,1.9,1.4,3.2,1.8,1.2.3,2.4.2,3.6.2,15.7,0,31.4,0,47,0,1.2,0,1.6.4,1.6,1.6Z" style="fill: #e6e6e6;"/>
			<text transform="translate(25.4 49.9) scale(1 1)" style="fill: #333; font-family: MicrosoftYaHeiUILight, &apos;Microsoft YaHei UI Light&apos;; font-size: 30.1px;"><tspan x="0" y="0">上传的文件</tspan></text>
			<text transform="translate(175.9 112.7) scale(1 1)" style="fill: #333; font-family: MicrosoftYaHeiUILight, &apos;Microsoft YaHei UI Light&apos;; font-size: 30.1px;"><tspan x="0" y="0">{filename}</tspan></text>
			<text transform="translate(176.7 153.6) scale(1 1)" style="fill: #4d4d4d; font-family: MicrosoftYaHeiUILight, &apos;Microsoft YaHei UI Light&apos;; font-size: 20.5px;"><tspan x="0" y="0">{filetime}</tspan></text>
			<text transform="translate(176.7 177.7) scale(1 1)" style="fill: #666; font-family: MicrosoftYaHeiUILight, &apos;Microsoft YaHei UI Light&apos;; font-size: 20.5px;"><tspan x="0" y="0">{filesize}</tspan></text>
			<rect x="47.5" y="91.6" width="38.1" height="1.4" rx=".5" ry=".5" style="fill: gray;"/>
			<rect x="47.5" y="112" width="38.1" height="1.4" rx=".5" ry=".5" style="fill: gray;"/>
			<rect x="47.5" y="130.3" width="63.7" height="1.4" rx=".5" ry=".5" style="fill: gray;"/>
			<text transform="translate(74.3 164.2)" style="fill: #e6e6e6; font-family: Calibri, Calibri; font-size: 24.5px;"><tspan x="0" y="0" style="letter-spacing: 0em;">C</tspan><tspan x="12.8" y="0" style="letter-spacing: 0em;">ODE</tspan></text>
			</svg>'''
	elif filetype == "text":
		svg = f'''<?xml version="1.0" encoding="UTF-8"?>
			<svg id="a" data-name="图层 1" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 655.1 224.1">
			<rect x="1.5" y="1.5" width="652.1" height="221.1" rx="17.2" ry="17.2" style="fill: #f2f2f2; stroke: #666; stroke-miterlimit: 10; stroke-width: 3px;"/>
			<path d="m139,152.4c0-1.9.3-3.8-.1-5.6-.6-2.9-2.2-4.8-5.2-5.6-1.7-.5-3.4-.3-5-.3-.8,0-1.1-.3-1.1-1.1-.2-8.9.5-17.9-.3-26.8-.1-1.4-.4-2.5-1.1-3.6-2.1-3-4.6-5.5-7-8.2-2.5-2.9-5-5.9-7.5-8.8-3.3-3.8-6.7-7.6-10-11.4-2.1-2.4-4.5-3.7-7.9-3.6-6.7.1-13.3,0-20,0h-16.2c-4.3,0-8.7,0-13,0-3.2,0-5.6,1.5-7.5,4-1.3,1.8-1.5,3.8-1.5,6,0,24.8,0,49.6,0,74.4,0,7.2-.5,14.4.3,21.5.3,2.4,1.5,4.1,3.1,5.6,2.3,2.1,5.1,2.8,8.4,2.8,17.6-.1,35.2,0,52.9,0s11.8,0,17.7,0c2.5,0,4.5-.9,6.4-2.5,2.3-2,2.9-4.6,3-7.4,0-2.8,0-5.5,0-8.3,0-1.3.4-1.7,1.7-1.6.9,0,1.9,0,2.8,0,3.9-.2,6.6-2.7,6.9-6.5.4-4.3,0-8.6.2-12.9Zm-42.8-70.6c.5-.2.8.3,1.1.6,1.9,1.9,3.5,3.9,5.2,5.9,1,1.1,1.8,2.4,3.1,3.2.6.3.7,1.2,1.2,1.7,2.4,2.7,4.8,5.3,6.9,8.2,1.3,1.7,2.7,3.3,4.1,4.8,1.5,1.5,2.2,3.6,4.3,4.7-.5.4-.8.3-1.1.3-6.6,0-13.2-.1-19.8,0-2.8,0-5.4-2.8-5.3-5.2,0-3.6,0-7.2,0-10.8s0-8.1,0-12.1c0-.4-.3-1,.3-1.2Zm27,100c0,3-2.1,5.7-5.6,5.6-.4,0-.8,0-1.2,0-22.9,0-45.8,0-68.7,0-1.8,0-3.5,0-5-1.2-1.8-1.4-3-3.1-2.6-5.5,0-.3,0-.5,0-.8,0-30.9,0-61.8,0-92.8,0-2,.4-3.5,2-4.7.9-.7,1.9-1,2.9-1,7.3,0,14.6,0,21.8,0,7.8,0,15.6,0,23.4,0,1.2,0,1.5.2,1.5,1.4,0,7.9,0,15.8,0,23.7,0,2.9,1.5,5,3.8,6.7,2.1,1.6,4.5,2.2,7.1,2.2,6.4,0,12.9,0,19.3,0,1,0,1.4.3,1.4,1.3,0,7.6,0,15.2,0,22.9,0,1.1-.3,1.3-1.4,1.3-8.2,0-16.3,0-24.5,0s-16,0-24,0c-3.3,0-5.6,1.5-7.1,4.4-.6,1.1-.4,2.2-.4,3.4,0,5.2.1,10.3,0,15.5,0,2.3.7,4.2,2.1,5.8.8.9,1.9,1.4,3.2,1.8,1.2.3,2.4.2,3.6.2,15.7,0,31.4,0,47,0,1.2,0,1.6.3,1.6,1.6,0,2.8,0,5.6,0,8.4Z" style="fill: #616b73;"/>
			<path d="m95.9,83c0-.4-.3-1,.3-1.2.5-.2.8.3,1.1.6,1.9,1.9,3.5,3.9,5.2,5.9,1,1.1,1.8,2.4,3.1,3.2.6.3.7,1.2,1.2,1.7,2.4,2.7,4.8,5.3,6.9,8.2,1.3,1.7,2.7,3.3,4.1,4.8,1.5,1.5,2.2,3.6,4.3,4.7-.5.4-.8.3-1.1.3-6.6,0-13.2-.1-19.8,0-2.8,0-5.4-2.8-5.3-5.2,0-3.6,0-7.2,0-10.8,0-4,0-8.1,0-12.1Z" style="fill: #e6e6e6;"/>
			<path d="m123.2,173.4c0,2.8,0,5.6,0,8.5,0,3-2.1,5.7-5.6,5.6-.4,0-.8,0-1.2,0-22.9,0-45.8,0-68.7,0-1.8,0-3.5,0-5-1.2-1.8-1.4-3-3.1-2.6-5.5,0-.3,0-.5,0-.8,0-30.9,0-61.8,0-92.7,0-2,.4-3.5,1.9-4.7.9-.7,1.9-1,2.9-1,7.3,0,14.6,0,21.8,0,7.8,0,15.6,0,23.4,0,1.1,0,1.5.2,1.5,1.4,0,7.9,0,15.8,0,23.6,0,2.9,1.5,5,3.8,6.7,2.1,1.6,4.5,2.2,7.1,2.2,6.4,0,12.9,0,19.3,0,1,0,1.4.3,1.4,1.3,0,7.6,0,15.2,0,22.9,0,1.1-.4,1.3-1.4,1.3-8.2,0-16.4,0-24.5,0s-16,0-24,0c-3.3,0-5.6,1.5-7.1,4.4-.6,1.1-.4,2.2-.4,3.4,0,5.2.1,10.3,0,15.5,0,2.3.7,4.2,2.1,5.9.8.9,1.9,1.4,3.2,1.8,1.2.3,2.4.2,3.6.2,15.7,0,31.4,0,47,0,1.2,0,1.6.4,1.6,1.6Z" style="fill: #e6e6e6;"/>
			<text transform="translate(25.4 49.9) scale(1 1)" style="fill: #333; font-family: MicrosoftYaHeiUILight, &apos;Microsoft YaHei UI Light&apos;; font-size: 30.1px;"><tspan x="0" y="0">上传的文件</tspan></text>
			<text transform="translate(175.9 112.7) scale(1 1)" style="fill: #333; font-family: MicrosoftYaHeiUILight, &apos;Microsoft YaHei UI Light&apos;; font-size: 30.1px;"><tspan x="0" y="0">{filename}</tspan></text>
			<text transform="translate(176.7 153.6) scale(1 1)" style="fill: #4d4d4d; font-family: MicrosoftYaHeiUILight, &apos;Microsoft YaHei UI Light&apos;; font-size: 20.5px;"><tspan x="0" y="0">{filetime}</tspan></text>
			<text transform="translate(176.7 177.7) scale(1 1)" style="fill: #666; font-family: MicrosoftYaHeiUILight, &apos;Microsoft YaHei UI Light&apos;; font-size: 20.5px;"><tspan x="0" y="0">{filesize}</tspan></text>
			<rect x="47.5" y="91.6" width="38.1" height="1.4" rx=".5" ry=".5" style="fill: gray;"/>
			<rect x="47.5" y="112" width="38.1" height="1.4" rx=".5" ry=".5" style="fill: gray;"/>
			<rect x="47.5" y="130.3" width="63.7" height="1.4" rx=".5" ry=".5" style="fill: gray;"/>
			<text transform="translate(83.6 164.2)" style="fill: #e6e6e6; font-family: Calibri, Calibri; font-size: 24.5px;"><tspan x="0" y="0">TXT</tspan></text>
			</svg>'''
	else:
		svg = "?"
	return Response(svg, media_type="image/svg+xml")

@app.post("/api/config")
def change_config(web: str, weather: str, date: str, markmap: str, sd: str):
	if web.lower() == "true":
		web_b = True
	else:
		web_b = False
	if sd.lower() == "true":
		sd_b = True
	else:
		sd_b = False
	if markmap.lower() == "true":
		markmap_b = True
	else:
		markmap_b = False
	if weather.lower() == "true":
		weather_b = True
	else:
		weather_b = False
	if date.lower() == "true":
		date_b = True
	else:
		date_b = False
	change_cfg(web=web_b, weather=weather_b, date=date_b, markmap=markmap_b, sd=sd_b, files=True)

@app.get("/api/sync")
def sync_config():
	cfg = get_config()
	weather = cfg['plugins']['0']['enable']
	date = cfg['plugins']['1']['enable']
	web = cfg['plugins']['2']['enable']
	markmap = cfg['plugins']['3']['enable']
	sd = cfg['plugins']['5']['enable']
	return Response(json.dumps({"web": web, "sd": sd, "markmap": markmap, "weather": weather, "date": date}), media_type="application/json")

@app.on_event("startup")
def startup_event():
	log('FRONT END STARTED', "EVENT")

@app.on_event("shutdown")
def shutdown_event():
	log('FRONT END SHUTDOWN', "EVENT")

if __name__ == "__main__":
	validate_config()
	uvicorn.run(app, host="0.0.0.0", port=8003)