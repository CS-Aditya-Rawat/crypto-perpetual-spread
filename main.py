import utils
import asyncio

async def process():
    while True:
        await utils.update_event.wait()
        print(utils.BINANCE_BID)
        print(utils.BINANCE_ASK)
        utils.update_event.clear()
        await asyncio.sleep(2)

if __name__ == "__main__":
    asyncio.run(process())
