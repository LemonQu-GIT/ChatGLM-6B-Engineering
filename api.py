from fastapi import FastAPI, Request
from pydantic import BaseModel
from typing import Optional
from sse_starlette.sse import EventSourceResponse
from transformers import AutoTokenizer, AutoModel
from plugins.utils import *
import uvicorn, json, torch, datetime

DEVICE = get_config()['basic']['device']
DEVICE_ID = get_config()['basic']['device_id']
model_name = get_config()['basic']['model']
quantize = get_config()['basic']['quantize']
CUDA_DEVICE = f"{DEVICE}:{DEVICE_ID}" if DEVICE_ID else DEVICE

def torch_gc():
	if torch.cuda.is_available():
		with torch.cuda.device(CUDA_DEVICE):
			torch.cuda.empty_cache()
			torch.cuda.ipc_collect()

app = FastAPI()

async def predict(prompt, max_length, top_p, temperature, history, suffix, prefix):
	global model, tokenizer
	given_response = ""
	for response, history in model.stream_chat(tokenizer, prompt, history, max_length=max_length, top_p=top_p, temperature=temperature):
		response = prefix + response
		given_response = response
		yield response
	yield given_response + suffix
	torch_gc()

class ConversationsParams(BaseModel):
	prompt: str
	max_length: Optional[int] = 2048
	top_p: Optional[float] = 0.7
	temperature: Optional[float] = 0.95
	suffix: Optional[str] = ""
	prefix: Optional[str] = ""
	history: list

@app.post('/stream')
async def conversations(params: ConversationsParams):
	predictGenerator = predict(params.prompt, params.max_length, params.top_p, params.temperature, params.history, params.suffix, params.prefix)
	now = datetime.datetime.now()
	time = now.strftime("%Y-%m-%d %H:%M:%S")
	log = "[" + time + "] " + '", params:"' + repr(params) + '"'
	print(log)
	return EventSourceResponse(predictGenerator)

@app.post("/default")
async def create_item(request: Request):
	global model, tokenizer
	json_post_raw = await request.json()
	json_post = json.dumps(json_post_raw)
	json_post_list = json.loads(json_post)
	prompt = json_post_list.get('prompt')
	history = json_post_list.get('history')
	max_length = json_post_list.get('max_length')
	top_p = json_post_list.get('top_p')
	temperature = json_post_list.get('temperature')
	response, history = model.chat(tokenizer,
								   prompt,
								   history=history,
								   max_length=max_length if max_length else 2048,
								   top_p=top_p if top_p else 0.7,
								   temperature=temperature if temperature else 0.95)
	now = datetime.datetime.now()
	time = now.strftime("%Y-%m-%d %H:%M:%S")
	answer = {
		"response": response,
		"history": history,
		"status": 200,
		"time": time
	}
	log = "[" + time + "] " + '", prompt:"' + prompt + '", response:"' + repr(response) + '"'
	print(log)
	torch_gc()
	return answer

@app.post("/ping")
async def ping():
	return "200"

@app.post("/forceclearmemory")
async def clear_memory():
	torch_gc()
	return "200"

if __name__ == '__main__':
	if DEVICE == "cuda":
		tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
		model = AutoModel.from_pretrained(model_name, trust_remote_code=True, device='cuda').quantize(quantize).half().cuda()
	else:
		tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
		model = AutoModel.from_pretrained(model_name, trust_remote_code=True).quantize(quantize).half().float()
	model.eval()
	uvicorn.run(app, host='0.0.0.0', port=get_config()['basic']['port'], workers=1)