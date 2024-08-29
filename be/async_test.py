from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import asyncio
import time

app = FastAPI()

# 비동기 큐 생성
request_queue = asyncio.Queue()
queue_lock = asyncio.Lock()

class RequestItem(BaseModel):
    data: str

async def process_queue():
    while True:
        # 큐에서 요청을 가져와서 처리
        async with queue_lock:
            request_item = await request_queue.get()
            if request_item is None:
                break
            await handle_request(request_item)
            request_queue.task_done()

async def handle_request(request_item: RequestItem):
    # 실제 요청 처리 (여기서는 간단히 sleep을 사용하여 처리 시간 시뮬레이션)
    print(f"Processing request with data: {request_item.data}")
    await asyncio.sleep(2)  # 요청 처리 시간 시뮬레이션
    print(f"Finished processing request with data: {request_item.data}")

@app.on_event("startup")
async def startup_event():
    # 큐를 처리할 작업자를 시작
    asyncio.create_task(process_queue())

@app.post("/process")
async def process_request(request_item: RequestItem):
    # 요청을 큐에 추가
    await request_queue.put(request_item)
    return {"message": "Request received and will be processed in order."}

@app.get("/status")
async def status():
    queue_size = request_queue.qsize()
    return {"queue_size": queue_size}
