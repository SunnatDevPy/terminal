# import json
# from fastapi import FastAPI, WebSocket
# from starlette.websockets import WebSocketDisconnect
#
from bot import bot
# from config import clients
#
# app = FastAPI()
#
#
# # === WebSocket-соединение для устройств ===
# @app.websocket("/ws/{device_id}")
# async def websocket_endpoint(websocket: WebSocket, device_id: str):
#     await websocket.accept()
#     clients[device_id] = websocket
#     print(f"📡 Устройство {device_id} подключилось")
#
#     try:
#         while True:
#             message = await websocket.receive_text()
#             if message == "ping":
#                 print(f"🔄 Пинг от {device_id}")
#                 continue
#
#             print(f"📩 Получено от {device_id}: {message}")
#             await bot.send_message(chat_id=5649321700, text=f"Сообщение от {device_id}: {message}")
#
#     except WebSocketDisconnect:
#         print(f"❌ Устройство {device_id} отключилось")
#         clients.pop(device_id, None)
#
#     except Exception as e:
#         print(f"⚠️ Ошибка WebSocket {device_id}: {e}")
#         clients.pop(device_id, None)
#
#
# # === API для отправки команд устройствам ===
# @app.post("/webhook")
# async def webhook(data: dict):
#     device_id = data.get("device_id")
#     message = json.dumps(data)
#
#     if device_id in clients:
#         await clients[device_id].send_text(message)
#         print(f"✅ Сообщение отправлено устройству {device_id}: {message}")
#         return {"status": "sent"}
#
#     return {"error": "device not connected"}

import json

from fastapi import FastAPI
from starlette.websockets import WebSocket

from bot import bot
from config import clients

app = FastAPI()


@app.websocket("/ws/{device_id}")
async def websocket_endpoint(websocket: WebSocket, device_id: str):
    await websocket.accept()
    clients[device_id] = websocket
    print(f"📡 Устройство {device_id} подключилось")

    try:
        while True:
            message = await websocket.receive_text()
            print(f"📩 Получено от {device_id}: {message}")
            # Отправка сообщения в Telegram (проверьте корректность chat_id)
            await bot.send_message(chat_id=5649321700, text=f"Сообщение от {device_id}: {message}")
    except Exception as e:
        print(f"❌ Устройство {device_id} отключилось: {e}")
        clients.pop(device_id, None)


# === 2. WEBHOOK для отправки сообщений на устройство ===
@app.post("/webhook")
async def webhook(data: dict):
    # Извлекаем device_id из входящих данных
    device_id = data.get("device_id")

    # Формируем структурированный payload
    payload = {
        "device_id": device_id,
        "action": data.get("action", "default_action"),  # Например, "PAYMENT" или другой тип команды
        "params": data.get("params", {})  # Дополнительные параметры команды
    }

    # Преобразуем словарь в JSON-строку
    message = json.dumps(payload)

    # Если устройство подключено (есть в clients), отправляем сообщение
    if device_id in clients:
        await clients[device_id].send_text(message)
        print(f"✅ Сообщение отправлено устройству {device_id}: {message}")
        return {"status": "sent"}

    return {"error": "device not connected"}

# === 3. API для просмотра подключенных устройств ===
@app.get("/devices")
async def list_devices():
    return {"connected_devices": list(clients.keys())}
