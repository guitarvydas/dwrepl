import py0dws as zd
import sys
import asyncio
import websockets
import json
import output
import subprocess

import echo

def initialize_hard_coded_test (arg):
    root_of_project = '.'
    root_of_0D = '.'
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

def interpretDiagram (arg):
    [palette, env] = initialize_hard_coded_test (arg)
    echo.install (palette)
    zd.start (palette, env)

############

inputBuffer = ""
filenameBuffer = ""

async def handler(websocket, path):
    global inputBuffer, filenameBuffer
    print("WebSocket connection established.")
    async for message in websocket:
        print (f'handler received {message}')
        data = json.loads(message)
        element_name = data['name']
        content = data ['content']

        if element_name == 'input' and content [-1] == '\n':
            output.reset ()
            print ("transpiling diagram")
            transpileDiagram ('test.drawio')
            print ("running diagram")
            interpretDiagram (inputBuffer)
            print ("sending output")

            # Respond with an update for the readonly textarea
            jsondumps = json.dumps({
                "output": output.get ("stdout"),
                "A": output.get ("A"),
                "B": output.get ("B"),
                "C": output.get ("C"),
            })
            print (f'sending {jsondumps}')
            print (output.buffers)
            response_message = jsondumps
            await websocket.send(response_message)
        elif element_name == 'input':
            inputBuffer = content
        elif element_name == 'filename':
            filenameBuffer = content

async def main():
    async with websockets.serve(handler, "localhost", 6789):
        print("Server started on ws://localhost:6789")
        await asyncio.Future()  # Run forever

# Run the server
asyncio.run(main())
