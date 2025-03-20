import json
from fastapi import FastAPI, WebSocket
from starlette.websockets import WebSocketDisconnect

from bot import bot
from config import clients

app = FastAPI()


# === WebSocket соединение для устройств ===
@app.websocket("/ws/{device_id}")
async def websocket_endpoint(websocket: WebSocket, device_id: str):
    await websocket.accept()
    clients[device_id] = websocket
    print(f"📡 Устройство {device_id} подключилось")

    try:
        while True:
            message = await websocket.receive_text()
            print(f"📩 Получено от {device_id}: {message}")

            # Отправляем сообщение в Telegram-бота
            await bot.send_message(chat_id=5649321700, text=f"Сообщение от {device_id}: {message}")

    except WebSocketDisconnect:
        print(f"❌ Устройство {device_id} отключилось")
        clients.pop(device_id, None)


# === API для отправки команд на устройства ===
@app.post("/webhook")
async def webhook(data: dict):
    device_id = data.get("device_id")
    message = json.dumps(data)

    if device_id in clients:
        await clients[device_id].send_text(message)
        print(f"✅ Сообщение отправлено устройству {device_id}: {message}")
        return {"status": "sent"}

    return {"error": "device not connected"}


# === API для просмотра подключенных устройств ===
@app.get("/devices")
async def list_devices():
    return {"connected_devices": list(clients.keys())}