"""
This Python program has a main routine called `repl`.

Repl creates one websocket called `guisocket`.
There are 2 coroutines called `gui` and `file_watcher`, respectively.
The code imports the function `compile_and_run` from Python module `compile_and_run.py`.
The function `compile_and_run` returns two strings called `stdout` and `stderr` respectively.
The coroutine `gui` waits for input from the `guisocket` websocket, then saves the input into a global variable called `input`, and, if the last character of the input is a newline, it calls `compile_and_run` and sends the resulting strings, as a single JSON object, to the `guisocket` websocket.
The coroutine `file_watcher` checks the modification time of a given file every 0.02 seconds. When the file is modified, `file_watcher` calls `compile_and_run` and sends the resulting strings, as a single JSON object, to the `guisocket` websocket.
"""

import asyncio
import websockets
import json
import os
from compile_and_run import compile_and_run

# Global variables
guisocket = None
input_data = None
file_to_watch = "test.drawio"  # Replace with the actual file you want to monitor

# Coroutine to handle incoming WebSocket messages and trigger compile_and_run
async def gui(websocket):
    global input_data
    async for message in websocket:
        input_data = message  # Store input in global variable

        # Check if the last character is a newline
        if input_data.endswith("\n"):
            # Run the compile_and_run function and capture output
            stdout, stderr = compile_and_run(input_data)
            
            # Send output as JSON back to the GUI WebSocket
            output = json.dumps({"stdout": stdout, "stderr": stderr})
            await websocket.send(output)

# Coroutine to monitor a file for modifications and trigger compile_and_run
async def file_watcher():
    last_mtime = os.path.getmtime(file_to_watch)
    while True:
        await asyncio.sleep(0.02)  # Check every 0.02 seconds

        # Get current modification time
        current_mtime = os.path.getmtime(file_to_watch)
        if current_mtime != last_mtime:  # File has been modified
            last_mtime = current_mtime  # Update last modification time
            
            # Run the compile_and_run function and capture output
            stdout, stderr = compile_and_run(input_data if input_data else "")
            
            # Send output as JSON to the GUI WebSocket if connected
            if guisocket:
                output = json.dumps({"stdout": stdout, "stderr": stderr})
                await guisocket.send(output)

# Main function to start the WebSocket server and run coroutines
async def repl():
    global guisocket
    async with websockets.serve(handle_connection, "localhost", 8765):
        await asyncio.gather(file_watcher())  # Run file_watcher in parallel

# Handle new WebSocket connections
async def handle_connection(websocket, path):
    global guisocket
    guisocket = websocket
    await gui(websocket)  # Run gui coroutine for this connection

# Run the main REPL function
asyncio.run(repl())
