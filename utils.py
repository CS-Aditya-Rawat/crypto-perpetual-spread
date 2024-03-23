# from okx import OkxRestClient
import os
import time
from signal import signal, SIGINT
from datetime import datetime
import json
import asyncio
from binance.um_futures import UMFutures
from binance.websocket.um_futures.websocket_client import UMFuturesWebsocketClient

# api = OkxRestClient(OKEX_API, OKEX_SECRET, 'RunorDie@1099')
BINANCE_BID = 0
BINANCE_ASK = 0
update_event = asyncio.Event()
def message_handler(_, message):
    global BINANCE_BID, BINANCE_ASK
    data = json.loads(message)
    BINANCE_BID = data['b'][0][0]
    BINANCE_ASK = data['a'][0][0]
    print(f"{datetime.now()} | {BINANCE_BID} | {BINANCE_ASK}")
    update_event.set()

def stop_client(sig, frame):
    print("Stopping WebSocket client...")
    my_client.stop()
    exit(0)


# Subscribe to a single symbol stream
# my_client.agg_trade(symbol="bnbusdt")
# my_client.mark_price(symbol="bchusdt", speed=1)
# my_client.mini_ticker(id=1, symbol="bchusdt")

if __name__ == "__main__":
    signal(SIGINT, stop_client)
    my_client = UMFuturesWebsocketClient(on_message=message_handler)
    my_client.partial_book_depth("bchusdt", level=5, speed=500)
    while True:
        try:
            time.sleep(0.5)
        except KeyboardInterrupt:
            stop_client(SIGINT, None)

