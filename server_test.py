
import asyncio
import websockets


async def handler(websocket):
    async for message in websocket:
        await websocket.send(message)


async def main():
    async with websockets.serve(handler, "", 8001):
        await asyncio.Future()  # run forever


if __name__ == "__main__":
    asyncio.run(main())