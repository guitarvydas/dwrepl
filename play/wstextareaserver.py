import asyncio
import websockets
import json

async def handler(websocket, path):
    print("WebSocket connection established.")
    async for message in websocket:
        data = json.loads(message)
        textarea_name = data['name']
        textarea_content = data['content']
        print(f"Received update from {textarea_name}: {textarea_content}")

async def main():
    async with websockets.serve(handler, "localhost", 6789):
        print("Server started on ws://localhost:6789")
        await asyncio.Future()  # Run forever

# Run the server
asyncio.run(main())
