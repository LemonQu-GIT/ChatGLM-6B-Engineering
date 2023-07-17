import argparse
from fastapi import FastAPI, Request
from pydantic import BaseModel
from typing import Optional
from sse_starlette.sse import EventSourceResponse
from transformers import AutoTokenizer, AutoModel
import uvicorn, json, torch, datetime

settings = {
	"device": "cuda",
	"device_id": "0",
}

def torch_gc():
	device = torch.device(f'{settings["device"]}:{settings["device_id"]}' if settings["device_id"] else settings["device"])
	if device == "cpu":
		return

	if torch.cuda.is_available():
		with torch.cuda.device(device):
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
	# parse arguments
	parser = argparse.ArgumentParser()
	parser.add_argument('--tokenizer', type=str)
	parser.add_argument('--model', type=str)
	parser.add_argument('--device', type=str, default='cuda')
	parser.add_argument('--device_id', type=str, default='0')
	parser.add_argument('--host', type=str, default='localhost')
	parser.add_argument('--port', type=int, default=8000)
	parser.add_argument('--workers', type=int, default=1)
	args = parser.parse_args()
 
	# check arguments
	if args.device not in ['cuda', 'cpu']:
		raise ValueError('Invalid device argument')

	if args.device == 'cuda':
		if args.device_id not in [str(i) for i in range(torch.cuda.device_count())]:
			raise ValueError('Invalid device_id argument')

	if args.model == '':
		raise ValueError('Invalid model argument')

	if args.tokenizer == '':
		raise ValueError('Invalid tokenizer argument')

	# set settings
	settings['device'] = args.device
	settings['device_id'] = args.device_id

	# load model
	tokenizer = AutoTokenizer.from_pretrained(args.tokenizer, trust_remote_code=True)
	model = AutoModel.from_pretrained(args.model, trust_remote_code=True)
	model = model.quantize(4)
	model = model.half()
	model = model.cuda()
	model.eval()
	print("Starting API server...")
	uvicorn.run(app, host=args.host, port=args.port, workers=args.workers)
