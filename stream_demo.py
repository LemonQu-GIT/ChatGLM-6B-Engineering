from fastapi import FastAPI, Response, Request
from fastapi.responses import StreamingResponse
import asyncio, time
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
origins = ["*"]
app.add_middleware(
	CORSMiddleware,
	allow_origins = origins,
	allow_credentials = True,
	allow_methods = ["*"],
	allow_headers = ["*"]
)

@app.get("/api/chat")
async def events(request: Request):
    async def event_generator():
        yield f"data: 1\n\n"
        time.sleep(1)
        yield f"data: 1\n\n"
        time.sleep(1)
        yield f"data: 1\n\n"
        time.sleep(1)
        yield f"data: [DONE]\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")

if __name__ == "__main__":
    import uvicorn
    #uvicorn.run("stream_api:app", host="0.0.0.0", port=8003, reload=True)
