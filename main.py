import py0dws as zd
import sys
import asyncio
import websockets
import json

import echo

def initialize_hard_coded_test ():
    root_of_project = '.'
    root_of_0D = '.'
    arg = 'testing...'
    main_container_name = 'main'
    diagram_names = ['test.drawio.json']
    palette = zd.initialize_component_palette (root_of_project, root_of_0D, diagram_names)
    return [palette, [root_of_project, root_of_0D, main_container_name, diagram_names, arg]]

def interpretDiagram ():
    [palette, env] = initialize_hard_coded_test ()
    echo.install (palette)
    zd.start (palette, env)

############

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
            interpretDiagram ()
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
