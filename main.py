import sys
import asyncio
import websockets
import json
import os
import time

import compile_and_run

inputBuffer = ""
filenameBuffer = ""

def run ():
    global inputBuffer, filenameBuffer
    r = compile_and_run.compile_and_run (filenameBuffer, inputBuffer)
    return r


# Path to the file to monitor for changes
FILE_PATH = "test.drawio"

# Last known modification time of the file
last_mod_time = None

# Routine 1: Check for file changes and send message to WebSocket 1
async def file_watcher(websocket_1):
    global last_mod_time
    sample_time = 0.02 # sample file every 20 msec
    print("Starting file watcher routine")

    while True:
        try:
            # Check file modification time
            current_mod_time = os.path.getmtime(FILE_PATH)
            if last_mod_time is None or current_mod_time != last_mod_time:
                print ("*** changed ***")
                last_mod_time = current_mod_time
                print("File modified. Running diagram")
                r = run ()
                j = json.dumps (r)
                await websocket_1.send (j)
                
            await asyncio.sleep(sample_time)
        
        except FileNotFoundError:
            print("File not found. Waiting for it to appear...")
            await asyncio.sleep(sample_time)  # Retry if the file doesn't exist

# Routine 2: Listen for messages from WebSocket 2 and respond
async def browser_ide(websocket):
    global inputBuffer, filenameBuffer
    print("Client connected to WebSocket 2")
    try:
        async for message in websocket:
            print(f"Received from WebSocket 2: {message}")
            data = json.loads(message)
            element_name = data['name']
            content = data ['content']

            if element_name == 'input' and (content != "" and content [-1] == '\n'):
                r = run ()
                j = json.dumps (r)
                await websocket.send (j)
            elif element_name == 'input':
                inputBuffer = content
            elif element_name == 'filename':
                filenameBuffer = content
    except websockets.ConnectionClosed:
        print("Client disconnected from WebSocket 2")

# WebSocket Server 1: Placeholder for file watcher to connect and send updates
async def websocket_1_server_handler(websocket):
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
