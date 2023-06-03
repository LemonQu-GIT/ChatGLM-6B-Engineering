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
chatmsg=  ""
latest_file = ""

@app.get("/api/chat")
async def chat_stream(prompt: str):
	global history, chatmsg, latest_file
	async def chat(prompt: str):
		global history, chatmsg, latest_file
		payload = {
				"input": prompt,
				"history": history
		}
		url = 'http://127.0.0.1:8000'
		response = requests.post(url, stream=True, json = payload)
		resp = ""
		add_text = "added!"
		for chunk in response.iter_content(chunk_size=1024):
			await asyncio.sleep(0.1)
			resp = chunk.decode('utf-8') + add_text
			yield resp
		chatmsg = resp.removeprefix("data: ")
		history.append([prompt, chatmsg])
		if len(history) > 10:
			history.pop(0)
		log(f"Chat history: {repr(history)}. Response: {repr(chatmsg)}")
	return StreamingResponse(chat(prompt), media_type="text/event-stream")
	
if __name__ == "__main__":
	import uvicorn
	uvicorn.run(app, host="0.0.0.0", port=8003)
