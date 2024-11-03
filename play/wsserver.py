import asyncio
import websockets

async def handler(websocket, path):
    while True:
        message = await websocket.recv()
        print(f"Received from client: {message}")
        await websocket.send("Message received")

        # Example: server sends a message every 3 seconds
        await asyncio.sleep(3)
        await websocket.send("Hello from the server!")

async def main():
    async with websockets.serve(handler, "localhost", 6789):
        print("Server running at ws://localhost:6789")
        await asyncio.Future()

asyncio.run(main())
