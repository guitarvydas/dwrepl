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
async def file_watcher(wsock):
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
                j = json.dumps (run ())
                await wsock.send (j)
                
            await asyncio.sleep(sample_time)
        
        except FileNotFoundError:
            print("File not found. Waiting for it to appear...")
            await asyncio.sleep(sample_time)  # Retry if the file doesn't exist

# Routine 2: Listen for messages from GUI and respond
async def browser_ide(wsock):
    global inputBuffer, filenameBuffer
    print("Client connected to GUI socket")
    try:
        async for message in wsock:
            print(f"Received from GUI: {message}")
            data = json.loads(message)
            element_name = data['name']
            content = data ['content']

            if element_name == 'input' and (content != "" and content [-1] == '\n'):
                j = json.dumps (run ())
                await wsock.send (j)
            elif element_name == 'input':
                inputBuffer = content
            elif element_name == 'filename':
                filenameBuffer = content
    except websockets.ConnectionClosed:
        print("Client disconnected from GUI")

# WebSocket Server 1: Placeholder for file watcher to connect and send updates
async def file_watcher_server_handler(websocket):
    print("file watcher server handler started")
    await file_watcher(websocket)

# Function to start both WebSocket servers
async def start_servers():
    # Start WebSocket Server 1 on port 8765 (for file watcher)
    file_watcher_server = await websockets.serve(file_watcher_server_handler, "localhost", 8765)
    print("file watcher WebSocket server started on ws://localhost:8765")

    # Start WebSocket Server 2 on port 8766 (for client communication)
    ide_server = await websockets.serve(browser_ide, "localhost", 8766)
    print("GUI websocket server started on ws://localhost:8766")

    # Keep both servers running indefinitely
    await asyncio.gather(file_watcher_server.wait_closed(), ide_server.wait_closed())

# Run the servers
asyncio.run(start_servers())
