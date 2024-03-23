import asyncio
import socketio
import json

sio = socketio.AsyncClient()

@sio.event()
async def connect():
    await sio.emit({
                    "method": "SUBSCRIBE",
                    "params": ["btcusdt@aggTrade"],
                    "id": 1
                   })
    print("Connected")

@sio.event()
async def msg_handler(_, data):
    print(data)

@sio.event()
async def disconnect():
    print("Disconnected")

@sio.event
async def main():
    BASE_URL = "wss://fstream.binance.com/ws/btcusdt@aggTrade"
    await sio.connect(BASE_URL)
    await sio.wait()

if __name__ == "__main__":
    asyncio.run(main())
