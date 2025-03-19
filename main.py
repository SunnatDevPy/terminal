import json

import uvicorn
from fastapi import FastAPI
from starlette.websockets import WebSocket

from bot import bot
from config import clients

app = FastAPI()


# === 4. ОБРАБОТКА WEBSOCKET ===
@app.websocket("/ws/{device_id}")
async def websocket_endpoint(websocket: WebSocket, device_id: str):
    await websocket.accept()
    clients[device_id] = websocket
    print(f"📡 Устройство {device_id} подключилось")

    try:
        while True:
            message = await websocket.receive_text()
            print(f"📩 Получено от {device_id}: {message}")

            from aiogram.utils import executor

            await bot.send_message(chat_id=5649321700, text=f"Сообщение от {device_id}: {message}")

    except:
        print(f"❌ Устройство {device_id} отключилось")
        del clients[device_id]


@app.post("/webhook")
async def webhook(data: dict):
    device_id = data.get("device_id")
    message = json.dumps(data)

    if device_id in clients:
        await clients[device_id].send_text(message)
        print(f"✅ Сообщение отправлено устройству {device_id}: {message}")
        return {"status": "sent"}

    return {"error": "device not connected"}


import json

import uvicorn
from fastapi import FastAPI
from starlette.websockets import WebSocket

from bot import bot
from config import clients

app = FastAPI()


# === 4. ОБРАБОТКА WEBSOCKET ===
@app.websocket("/ws/{device_id}")
async def websocket_endpoint(websocket: WebSocket, device_id: str):
    print(device_id)
    print(websocket)
    await websocket.accept()
    clients[device_id] = websocket
    print(f"📡 Устройство {device_id} подключилось")

    try:
        while True:
            message = await websocket.receive_text()
            print(f"📩 Получено от {device_id}: {message}")

            await bot.send_message(chat_id=5649321700, text=f"Сообщение от {device_id}: {message}")

    except Exception as e:
        print(f"❌ Устройство {device_id} отключилось")
        del clients[device_id]


@app.post("/webhook")
async def webhook(data: dict):
    device_id = data.get("device_id")
    message = json.dumps(data)

    if device_id in clients:
        await clients[device_id].send_text(message)
        print(f"✅ Сообщение отправлено устройству {device_id}: {message}")
        return {"status": "sent"}

    return {"error": "device not connected"}
