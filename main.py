import py0dws as zd
import sys
import asyncio
import websockets
import json
import output
import subprocess

import echo

def initialize_hard_coded_test ():
    root_of_project = '.'
    root_of_0D = '.'
    arg = 'pt was here...'
    main_container_name = 'main'
    diagram_names = ['test.drawio.json']
    palette = zd.initialize_component_palette (root_of_project, root_of_0D, diagram_names)
    return [palette, [root_of_project, root_of_0D, main_container_name, diagram_names, arg]]

def transpileDiagram (fname):
    ret = subprocess.run (['/Users/paultarvydas/Documents/projects-icloud/dwrepl/das2json/mac/das2json', f'{fname}'], capture_output=True, encoding='utf-8')
    if  not (ret.returncode == 0):
        if ret.stderr != None:
            output.stderr (ret.stderr)
        else:
            output.append ("stderr", f"error in shell_out {ret.returncode}")
    else:
        return output.append ("stdout", ret.stdout)

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
        content = ''

        if element_name == 'goButton':
            output.reset ()
            print ("transpiling diagram")
            transpileDiagram ('test.drawio')
            print ("running diagram")
            interpretDiagram ()
            print ("sending output")
            content = output.get ("stdout")

            # Respond with an update for the readonly textarea
            response_message = json.dumps({
                "name": "output",
                "content": f"{content}"
            })
            await websocket.send(response_message)

async def main():
    async with websockets.serve(handler, "localhost", 6789):
        print("Server started on ws://localhost:6789")
        await asyncio.Future()  # Run forever

# Run the server
asyncio.run(main())
