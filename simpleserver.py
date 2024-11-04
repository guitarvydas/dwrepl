import asyncio
import websockets
import json

async def handler(websocket, path):
    n = 0
    while True:
        print("WebSocket connection established.")
        message = json.dumps({
            "name": "output",
            "fluff": "fluff",
            "content": f"Hello! {n}"
        })
        await websocket.send(message)
        print ("handler done")
        await asyncio.sleep (2)
        print ("waking up")
        n += 1
        
async def main():
    async with websockets.serve(handler, "localhost", 6789):
        print("Server started on ws://localhost:6789")
        await asyncio.Future()  # Run forever
        print ("main finished")

# Run the server
asyncio.run(main())
