import json, uvicorn, requests, base64, os, time, pdfplumber, datetime
from PIL import Image, PngImagePlugin
from fastapi import FastAPI, Query, Response, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from front_end_utils import *
from zhdate import ZhDate
import asyncio

app = FastAPI()
origins = ["*"]
app.add_middleware(
	CORSMiddleware,
	allow_origins = origins,
	allow_credentials = True,
	allow_methods = ["*"],
	allow_headers = ["*"]
)

history = []
latest_file = ""
chat_prompt = ""
chat_reponse=  ""

@app.get("/api/repeat")
def repeat():
	try:
		global history, chat_reponse
		log(f'Chat message: {repr(chat_reponse)} requests to repeat')
		request = chatglm_json(str(chat_reponse), history=history)
		request_list = json.loads(request)
		response = request_list.get('response')
		log(f'Chat message: {repr(chat_reponse)} repeats finished. Response: {repr(response)}')
		return Response(f"{response}")
	except:
		log('Error while repeating chat message')
		return Response("<font color=#e54240>Something went wrong...</font>")

@app.get("/api/chat")
async def chat_stream(prompt: str):
	global history, chat_reponse, latest_file, chat_prompt
	async def chat(prompt: str):
		global history, chat_reponse, latest_file, chat_prompt
		chat_prompt = prompt
		if not latest_file == "":
			suffix = get_suffix(latest_file)
			log(f"Input file suffix: {suffix}")
		else:
			suffix = "Undefined"
   
		if get_config()['SD']['enable'] == "True":
			request = chatglm_json(str(f"我的问题是“{prompt}”，请选出下列内容中最符合的一项 A. 聊天  B.画图，请直接回复答案（A或B），不需要回复原因"), history=[])
			chat_reponse = prompt
			request_list = json.loads(request)
			response = request_list.get('response')
		else:
			response = 'A'
		if 'B' in response and get_config()['SD']['enable'] == "True":
			type = "stable_diffusion"
			log('Decide to go on Stable Diffusion job')
		elif 'A' in response or get_config()['SD']['enable'] == "False":
			type = "conversation"
			log('Decide to go on ChatGLM-6B job')
		else:
			type = "conversation"
			log('Decide to go on ChatGLM-6B job')
		
		if type == "conversation":
			additional_info = ""
			if if_trigger_additional_info(prompt, "date"):
				now = datetime.datetime.now()
				date_time = now.strftime("%Y年%m月%d日 %H点%M分%S秒")
				additional_info += f"\n已知现在的日期及时间为{date_time}，"
			if if_trigger_additional_info(prompt, "zh_date"):
				today = datetime.datetime.today()
				zh_date = ZhDate.from_datetime(datetime.datetime(today.year, today.month, today.day)).chinese()
				additional_info += f"\n已知现在的农历日期为{zh_date}，"
			if if_trigger_additional_info(prompt, "weather"):
				if '预' in prompt or '明天' in prompt:
					city = weather_search_local(prompt)
					id = weather_search_city(city)
					info = json.dumps(weather_get_tmr(id), ensure_ascii=False)
					info = json.loads(info)
					temp_max = info['tempMax']
					temp_min = info['tempMin']
					text_day = info['textDay']
					text_night = info['textNight']
					wind_dir_day = info['windDirDay']
					wind_scale_day = info['windScaleDay']
					wind_dir_night = info['windDirNight']
					wind_scale_night = info['windScaleNight']
					additional_info += f"\n已知明天{city}最高温度为{temp_max}摄氏度，最低温度为{temp_min}摄氏度，白天天气为{text_day}，吹{wind_scale_day}级{wind_dir_day}；晚上天气为{text_night}，吹{wind_scale_night}级{wind_dir_night}，"
				else:
					city = weather_search_local(prompt)
					id = weather_search_city(city)
					info = json.dumps(weather_get(id), ensure_ascii=False)
					info = json.loads(info)
					temp = info['now']['temp']
					text = info['now']['text']
					wind_dir = info['now']['windDir']
					wind_scale = info['now']['windScale']
					additional_info += f"\n已知现在{city}天气为{text}，温度为{temp}摄氏度，吹{wind_scale}级{wind_dir}，"
			log(f'Additional Info: {additional_info}')

			if if_trigger_web(prompt) and get_config()['Web']['enable'] == "True":
				feature = get_config().get('Web').get('feature')
				log(f'Begin searching job. Feature: {feature}')
				search_resp = search_main(str(prompt), feature)
				web_info = search_resp[1]
				references = search_resp[0]
				if len(str(web_info)) > 2000:
					web_info = web_info[0:2000]
				log(f'Search finished. Web search response: {repr(search_resp)}')
				await asyncio.sleep(0.1)
				ask_prompt = additional_info + f'我的问题是“{prompt}”\n我在网络上查询到了一些网络上的参考信息“{web_info}”\n请根据我的问题，参考我给与的信息以及你的理解进行回复'
				preview_reference = generate_reference(references)			
				payload = {
					"input": ask_prompt,
					"history": history,
					"additional": f"\n{preview_reference}"
				}
				url = f"{get_config()['basic']['host']}:{get_config()['basic']['port']}/stream"
				response = requests.post(url, stream=True, json = payload)
				resp = ""
				for chunk in response.iter_content(chunk_size=1024):
					await asyncio.sleep(0.1)
					resp = f"{chunk.decode('utf-8', 'ignore')}"
					yield resp 
				chat_reponse = resp.replace("data: ", "")
				history.append([chat_prompt, repr(chat_reponse)])
				if len(history) > 10:
					history.pop(0)
				log(f"Chat history: {repr(history)}. Response: {repr(chat_reponse)}")
			else:
				log(f"Input file: {repr(latest_file)}")
				if suffix in ['.txt','.java','.py','.c','.cpp','.']:
					folder = os.getcwd()
					with open(folder + "\\src\\assets\\files\\"+str(latest_file), "r", encoding="utf-8") as f:
						content = f.read()
					log(f'Input text content: {repr(content)}')
					if suffix == ".py":
						file_type = "python"
					else:
						file_type = suffix[1:]
					preview_content = preview_text(content, file_type)
					ask_prompt = str(additional_info + f"上传的文件内容为“{content}”，我的问题是：{prompt}，请根据文件的内容及我的问题及你的思考给出回复")
					payload = {
						"input": ask_prompt,
						"history": history
					}
					url = f"{get_config()['basic']['host']}:{get_config()['basic']['port']}/stream"
					response = requests.post(url, stream=True, json = payload)
					resp = ""
					for chunk in response.iter_content(chunk_size=1024):
						await asyncio.sleep(0.1)
						resp = chunk.decode('utf-8', 'ignore') +"\n"+ preview_content
						yield resp 
					chat_reponse = resp.replace("data: ", "")
					history.append([chat_prompt, chat_reponse])
					if len(history) > 10:
						history.pop(0)
					log(f"Chat history: {repr(history)}. Response: {repr(chat_reponse)}")
				elif suffix in ['.png','.jpg','.jfif','.jpeg']:
					folder = os.getcwd()
					image_detail = clip_trans(clip_image(folder + "\\src\\assets\\files\\" + str(latest_file)))
					print(image_detail)
					ask_prompt = str(additional_info + f"上传的文件内容为“{image_detail}”，我的问题是：{prompt}，请根据文件的内容及我的问题及你的思考给出回复")
				elif suffix == '.pdf':
					folder = os.getcwd()
					content = ""
					with pdfplumber.open(folder + "\\src\\assets\\files\\" + str(latest_file)) as pdf:
						for page in pdf.pages:
							content += page.extract_text()
					log(f"Input PDF content: {repr(content)}")
					ask_prompt = str(additional_info + f"上传的pdf文件内容为“{content}”，我的问题是：{prompt}，请根据pdf文件的内容及我的问题及你的思考给出回复")
				else:
					if additional_info == "":
						ask_prompt = prompt
					else:
						ask_prompt = str(additional_info + f"我的问题是：{prompt}，请根据已知信息及我的问题及你的思考给出回复")
				payload = {
					"input": ask_prompt,
					"history": history
				}
				url = f"{get_config()['basic']['host']}:{get_config()['basic']['port']}/stream"
				response = requests.post(url, stream=True, json = payload)
				resp = ""
				for chunk in response.iter_content(chunk_size=1024):
					await asyncio.sleep(0.1)
					resp = chunk.decode('utf-8', 'ignore')
					yield resp
				chat_reponse = resp.replace("data: ", "")
				history.append([chat_prompt, chat_reponse])
				if len(history) > 10:
					history.pop(0)
				log(f"Chat history: {repr(history)}. Response: {repr(chat_reponse)}")
	
		elif type == "stable_diffusion":
			if bool(get_config()['SD']['enable']):
				if suffix == ".txt":
					folder = os.getcwd()
					with open(folder + "\\src\\assets\\files\\"+str(latest_file), "r", encoding="utf-8") as f:
						content = f.read()
					log(f'Input text content: {content}')
					prompt_history = [["我接下来会给你一些作画的指令，你只要回复出作画内容及对象，不需要你作画，不需要给我参考，不需要你给我形容你的作画内容，请根据所给的文件的内容，给出作画的内容，你不要回复“好的，我会画一张”等不必要的内容，你只需回复作画内容。你听懂了吗","听懂了。请给我一些作画的指令。"]]
					request = chatglm_json(str(f"不需要你作画，不需要给我参考，不需要你给我形容你的作画内容，我上传的文件内容是{content}，请根据所给的文件的内容，给出“{prompt}”中的作画内容，请直接给出作画内容和对象"), prompt_history)
				else:
					prompt_history = [["我接下来会给你一些作画的指令，你只要回复出作画内容及对象，不需要你作画，不需要给我参考，不需要你给我形容你的作画内容，请直接给出作画内容，你不要回复“好的，我会画一张”等不必要的内容，你只需回复作画内容。你听懂了吗","听懂了。请给我一些作画的指令。"]]
					request = chatglm_json(str(f"不需要你作画，不需要给我参考，不需要你给我形容你的作画内容，请给出“{prompt}”中的作画内容，请直接给出作画内容和对象"), prompt_history)
				request_list = json.loads(request)
				draw_object = request_list.get('response')
				if draw_object[0] == "，" or draw_object[0] == "," or draw_object[0] == "。" or draw_object[0] == ".":
					draw_object = draw_object[1:len(draw_object)]
				if draw_object[-1] == "，" or draw_object[-1] == "," or draw_object[-1] == "。" or draw_object[-1] == ".":
					draw_object = draw_object[0:len(draw_object)-1]
				draw_object = draw_object.replace("好的", "")
				draw_object = draw_object.replace("我", "")
				draw_object = draw_object.replace("将", "")
				draw_object = draw_object.replace("会", "")
				draw_object = draw_object.replace("画", "")
				if draw_object[0] == "，" or draw_object[0] == "," or draw_object[0] == "。" or draw_object[0] == ".":
					draw_object = draw_object[1:len(draw_object)]
				if draw_object[-1] == "，" or draw_object[-1] == "," or draw_object[-1] == "。" or draw_object[-1] == ".":
					draw_object = draw_object[0:len(draw_object)-1]
				draw = str(translate(draw_object))
				log(f"Draw object: {draw}")
				stable_diffusion(draw,"",get_config()['SD']['steps'])
				request = chatglm_json(f"请介绍一下你画的关于{draw_object}", prompt_history)
				request_list = json.loads(request)
				detail = request_list.get('response')
				history.append([chat_prompt, chat_reponse])
				if len(history) > 10:
					history.pop(0)
				log(f"Chat history: {repr(history)}. Response: {repr(chat_reponse)}")
				yield '[SD IMAGE]'+str(detail)
	return StreamingResponse(chat(prompt), media_type="text/event-stream")
	
@app.post("/api/stop")
def stop():
	log('User Interrupt')
	return Response("User Interrupt")

@app.post("/api/delete")
def delete():
	global chat_reponse, latest_file, history
	chat_reponse = []
	latest_file = ""
	history = []
	log('User history deleted')

@app.get("/api/sdimg")
def image():
	log('Get stable diffusion image')
	data = open('./src/assets/imgs/stable_diffusion.png', mode="rb")
	return StreamingResponse(data, media_type="image/png")

@app.post("/api/upload")
async def upload_file(file: UploadFile = File(...)):
	contents = await file.read()
	folder = os.getcwd()
	print(file.content_type)
	with open(folder + "\\src\\assets\\files\\"+str(file.filename), "wb") as f:
		f.write(contents)
	global latest_file
	latest_file = str(file.filename)
	log(f"Uploaded files, filename: {latest_file}")

@app.get("/api/title")
def title():
	global chat_reponse, chat_prompt
	request = chatglm_json(f"我的问题是：“{chat_prompt}”，请对我发送的内容进行概括，8个字以内，请直接回复概括内容，不需要回复其他内容", [])
	request_list = json.loads(request)
	title_text = str(request_list.get('response'))
	title_text = title_text.strip().replace("概括内容","").replace("概括文字","").replace("概括","").replace("：","").replace(":","").removesuffix("。").removesuffix(".").removesuffix("，").removesuffix(",")
	return Response(title_text)


@app.on_event("startup")
def startup_event():
    log('FRONT END STARTED')
    
@app.on_event("shutdown")
def shutdown_event():
    log('FRONT END SHUTDOWN')

if __name__ == "__main__":
	import uvicorn
	uvicorn.run(app, host="0.0.0.0", port=8003)