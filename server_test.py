
import asyncio
import json
import time
import random
import websockets


async def handler(websocket):
  print("handler called")
  while True:
    obj = {
      "positions":[
        {"x": random.uniform(0, 100), "y":random.uniform(0, 100)}
      ]
    }
    await websocket.send(json.dumps(obj))
    time.sleep(0.5)
  # async for message in websocket:
  #     await websocket.send(message)


async def main():
  async with websockets.serve(handler, "", 8001):
    await asyncio.Future()  # run forever


if __name__ == "__main__":
  asyncio.run(main())