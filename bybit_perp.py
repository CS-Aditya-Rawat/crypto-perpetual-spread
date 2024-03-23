from pybit.unified_trading import WebSocket
from logging.handlers import RotatingFileHandler
import asyncio
from datetime import datetime
import json
from okx import OkxSocketClient
import logging

OKEX_API = "45265658-5255-4f80-a1dd-98ccb9051c26"
OKEX_SECRET = "6E3DA21805CF0837DAF22022330C0D90"

bybit_close = None
okex_close = None
okex_ask = None
okex_bid = None
bybit_ask = None
bybit_bid = None
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

file_handler = RotatingFileHandler("app.log", maxBytes=1024 * 1024, backupCount=5)
file_handler.setLevel(logging.INFO)
formatter = logging.Formatter("%(message)s")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


def ws_handler(s):
    global okex_close, okex_ask, okex_bid
    data = json.loads(s)

    if "event" in data:
        if data["event"] == "subscribe":
            print("Subscribed")
            return
        if data["event"] == "unsubscribe":
            print("Unsubscribed")
            return

    if "arg" in data and "channel" in data["arg"]:
        channel = data["arg"]["channel"]
        symbol = data["arg"]["instId"]
        if channel == "tickers":
            ticker = data["data"][0]
            okex_close = ticker["last"]
            okex_ask = ticker["askPx"]
            okex_bid = ticker["bidPx"]
        else:
            print(f"[UNKNOWN] {text}")


async def okx_tickers():
    ws = OkxSocketClient()
    await ws.public.start()
    await ws.public.subscribe(
        [{"channel": "tickers", "instId": "SOL-USDT-SWAP"}], callback=ws_handler
    )


ws = WebSocket(
    testnet=False,
    channel_type="linear",
)


def handle_message(message):
    global bybit_close, bybit_ask, bybit_bid
    data = message["data"]
    bybit_close = data["markPrice"]
    bybit_ask = data["ask1Price"]
    bybit_bid = data["bid1Price"]


ws.ticker_stream(symbol="SOLUSDT", callback=handle_message)


async def print_rate():
    while True:
        if bybit_ask is not None and okex_bid is not None:
            logger.info(
                f"{datetime.now()} | OKX: {okex_ask} | BYBIT: {bybit_bid} | {round(float(bybit_bid)-float(okex_ask), 6)} | {round(float(okex_bid) - float(bybit_ask), 6)}"
            )
        await asyncio.sleep(0.5)


async def main():
    tasks = [okx_tickers(), print_rate()]
    await asyncio.gather(*tasks)


asyncio.run(main())
