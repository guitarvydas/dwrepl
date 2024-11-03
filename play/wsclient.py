import asyncio
import websockets

async def listen():
    uri = "ws://localhost:6789"
    async with websockets.connect(uri) as websocket:
        await websocket.send("Hello, from Client!")
        
        # Continuously listen for messages from the server
        while True:
            response = await websocket.recv()
            print(f"Received from server: {response}")
            await websocket.send("more Hello, from Client!")

asyncio.run(listen())
