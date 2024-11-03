import asyncio
import websockets
import json

async def handler(websocket, path):
    print("WebSocket connection established.")
    async for message in websocket:
        data = json.loads(message)
        element_name = data['name']
        element_content = data['content']
        name = ''
        content = ''
        if element_name == 'goButton':
            name = 'go'
            content = '<button pressed>'
        else:
            name = element_name
            content = element_content
        print(f"Received update from {name}: {content}")

        # Respond with an update for the readonly textarea
        response_message = json.dumps({
            "name": "output",
            "content": f"Python received: {name}:{content}"
        })
        await websocket.send(response_message)

async def main():
    async with websockets.serve(handler, "localhost", 6789):
        print("Server started on ws://localhost:6789")
        await asyncio.Future()  # Run forever

# Run the server
asyncio.run(main())
