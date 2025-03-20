import json
from fastapi import FastAPI, WebSocket
from starlette.websockets import WebSocketDisconnect

from bot import bot
from config import clients

app = FastAPI()


# === WebSocket-соединение для устройств ===
@app.websocket("/ws/{device_id}")
async def websocket_endpoint(websocket: WebSocket, device_id: str):
    await websocket.accept()
    clients[device_id] = websocket
    print(f"📡 Устройство {device_id} подключилось")

    try:
        while True:
            message = await websocket.receive_text()
            if message == "ping":
                print(f"🔄 Пинг от {device_id}")
                continue

            print(f"📩 Получено от {device_id}: {message}")
            await bot.send_message(chat_id=5649321700, text=f"Сообщение от {device_id}: {message}")

    except WebSocketDisconnect:
        print(f"❌ Устройство {device_id} отключилось")
        clients.pop(device_id, None)

    except Exception as e:
        print(f"⚠️ Ошибка WebSocket {device_id}: {e}")
        clients.pop(device_id, None)


# === API для отправки команд устройствам ===
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