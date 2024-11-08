import py0dws as zd
import sys
import asyncio
import websockets
import json
import output
import subprocess
import os
import time

import echo


def initialize_hard_coded_test (arg):
    palette = zd.initialize_component_palette ('.', '.', ['test.drawio.json'])
    return [palette, ['.', '.', 'main', ['test.drawio.json'], arg]]

def transpileDiagram (fname):
    ret = subprocess.run (['./das2json/mac/das2json', f'{fname}'], capture_output=True, encoding='utf-8')
    if  not (ret.returncode == 0):
        if ret.stderr != None:
            output.append ("stderr", ret.stderr)
        else:
            output.append ("stderr", f"error in shell_out {ret.returncode}")
    else:
        return output.append ("stdout", ret.stdout)

def interpretDiagram (arg):
    [palette, env] = initialize_hard_coded_test (arg)
    echo.install (palette)
    zd.start (palette, env)




# Path to the file to monitor for changes
FILE_PATH = "test.drawio"

# Last known modification time of the file
last_mod_time = None

# Routine 1: Check for file changes and send message to WebSocket 1
async def file_watcher(websocket_1):
    global last_mod_time
    print("Starting file watcher routine")

    while True:
        try:
            # Check file modification time
            current_mod_time = os.path.getmtime(FILE_PATH)
            if last_mod_time is None or current_mod_time != last_mod_time:
                last_mod_time = current_mod_time
                print("File modified. Sending update to WebSocket 1")
                
                # Send a notification to WebSocket 1
                await websocket_1.send("File has been modified")
                
            # Check for changes every 2 seconds
            await asyncio.sleep(2)
        
        except FileNotFoundError:
            print("File not found. Waiting for it to appear...")
            await asyncio.sleep(2)  # Retry if the file doesn't exist

# Routine 2: Listen for messages from WebSocket 2 and respond
async def browser_ide(websocket, path):
    print("Client connected to WebSocket 2")
    try:
        async for message in websocket:
            print(f"Received from WebSocket 2: {message}")
            data = json.loads(message)
            element_name = data['name']
            content = data ['content']

            if element_name == 'input' and (content != "" and content [-1] == '\n'):
                output.reset ()
                print (f'transpiling diagram {filenameBuffer}')
                transpileDiagram (filenameBuffer)
                print (f'running diagram {output.buffers}')
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
    except websockets.ConnectionClosed:
        print("Client disconnected from WebSocket 2")

# WebSocket Server 1: Placeholder for file watcher to connect and send updates
async def websocket_1_server_handler(websocket, path):
    print("WebSocket 1 server handler started")
    await file_watcher(websocket)

# Function to start both WebSocket servers
async def start_servers():
    # Start WebSocket Server 1 on port 8765 (for file watcher)
    file_watcher_server = await websockets.serve(websocket_1_server_handler, "localhost", 8765)
    print("WebSocket 1 server started on ws://localhost:8765")

    # Start WebSocket Server 2 on port 8766 (for client communication)
    ide_server = await websockets.serve(browser_ide, "localhost", 8766)
    print("WebSocket 2 server started on ws://localhost:8766")

    # Keep both servers running indefinitely
    await asyncio.gather(file_watcher_server.wait_closed(), ide_server.wait_closed())

# Run the servers
asyncio.run(start_servers())
