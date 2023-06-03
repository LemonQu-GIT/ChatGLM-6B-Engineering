from fastapi import FastAPI, Request
from pydantic import BaseModel
from typing import Optional
from sse_starlette.sse import EventSourceResponse
from transformers import AutoTokenizer, AutoModel
import uvicorn, json, torch, datetime

DEVICE = "cuda"
DEVICE_ID = "0"
CUDA_DEVICE = f"{DEVICE}:{DEVICE_ID}" if DEVICE_ID else DEVICE

def torch_gc():
	if torch.cuda.is_available():
		with torch.cuda.device(CUDA_DEVICE):
			torch.cuda.empty_cache()
			torch.cuda.ipc_collect()

app = FastAPI()

async def predict(input, max_length, top_p, temperature, history, additional):
	global model, tokenizer
	given_response = ""
	for response, history in model.stream_chat(tokenizer, input, history, max_length=max_length, top_p=top_p, temperature=temperature):
		given_response = response
		yield response
	yield given_response + additional
	torch_gc()

class ConversationsParams(BaseModel):
	input: str
	max_length: Optional[int] = 2048
	top_p: Optional[float] = 0.7
	temperature: Optional[float] = 0.95
	additional: Optional[str] = ""
	history: list

@app.post('/stream')
async def conversations(params: ConversationsParams):
	history = list(map(tuple, params.history))
	predictGenerator = predict(params.input, params.max_length, params.top_p, params.temperature, params.history, params.additional)
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

if __name__ == '__main__':
    #tokenizer = AutoTokenizer.from_pretrained("THUDM/chatglm-6b", trust_remote_code=True)
	#model = AutoModel.from_pretrained("THUDM/chatglm-6b", trust_remote_code=True).quantize(4).half().cuda()
	tokenizer = AutoTokenizer.from_pretrained(r"E:\huggingface\models--THUDM--chatglm-6b\snapshots\a10da4c68b5d616030d3531fc37a13bb44ea814d", trust_remote_code=True)
	model = AutoModel.from_pretrained(r"E:\huggingface\models--THUDM--chatglm-6b\snapshots\a10da4c68b5d616030d3531fc37a13bb44ea814d", trust_remote_code=True).quantize(4).half().cuda()
	model.eval()
	uvicorn.run(app, host='0.0.0.0', port=8000, workers=1)