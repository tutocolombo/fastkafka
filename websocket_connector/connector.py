import asyncio
import json

import requests
import websockets


async def handler(ws):
    while True:
        message = await ws.recv()
        requests.post("http://127.0.0.1:8000/producer", json=json.loads(message))


async def main():
    url = "wss://ws.coincap.io/trades/binance"
    async with websockets.connect(url) as ws:
        await handler(ws)
        await asyncio.Future()  # run forever


if __name__ == "__main__":
    asyncio.run(main())
