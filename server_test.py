
import asyncio
import json
import time
import random
import websockets

from vision import capture


async def handler(websocket):
  print("handler called")

  async def handle_position_data(pos):
    if pos:
      x = pos[0]
      y = 50 #pos[1]
      print(x)
      print(y)
      obj = {
        "positions":[
          {"x": x, "y":y}
        ]
      }
      await websocket.send(json.dumps(obj))

  
  while True:
    coords = capture()
    print(coords)
    await handle_position_data(coords)


async def main():
  async with websockets.serve(handler, "", 8001):
    await asyncio.Future()  # run forever


if __name__ == "__main__":
  asyncio.run(main())