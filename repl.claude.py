"""
This program implements a REPL system with the following components:
- Two websockets: to_gui (8765) and from_gui (8766)
- Two coroutines: gui and file_watcher
- Monitors test.drawio for changes
- Handles JSON input from GUI
- Compiles and runs code based on file changes or GUI input
- Sends results back to GUI as JSON
"""

import asyncio
import websockets
import json
import os
import time
from compile_and_run import compile_and_run

# Global variables
file_being_watched = "test.drawio"
input_from_gui = None
last_mod_time = 0
to_gui = None
from_gui = None

def haskey (d, k):
    if k in d:
        return True
    else:
        return False
    
async def handle_to_gui(websocket):
    global to_gui
    to_gui = websocket
    try:
        await websocket.wait_closed()
    finally:
        to_gui = None

async def handle_from_gui(websocket):
    global from_gui
    from_gui = websocket
    try:
        await websocket.wait_closed()
    finally:
        from_gui = None

async def gui():
    global input_from_gui
    
    while True:
        try:
            if from_gui is None:
                await asyncio.sleep(0.1)
                continue

            # Wait for input from GUI
            message = await from_gui.recv()
            input_from_gui = json.loads(message)
            print (f'from_gui {input_from_gui}')
            v = input_from_gui.keys()
            w = haskey(input_from_gui, 'input')
            ww = None
            if "input" in input_from_gui:
                ww = True
            else:
                ww = False
            x = input_from_gui['input'].endswith("\n")
            print (f'  {v} {w} {ww} {x}')
            
            # Check if input exists and ends with newline
            if to_gui and haskey(input_from_gui, 'input') and input_from_gui ['input'].endswith('\n'):
                # Run compiler with input from GUI
                result = compile_and_run(
                    file_being_watched,
                    input_from_gui ['input'] if haskey(input_from_gui, 'input') else ""
                )
                
                # Send result to GUI
                await to_gui.send(json.dumps(result))
                
        except websockets.exceptions.ConnectionClosed:
            continue
        except Exception as e:
            print(f"Error in gui coroutine: {e}")

async def file_watcher():
    global last_mod_time
    
    while True:
        try:
            if to_gui is None:
                await asyncio.sleep(0.1)
                continue

            current_mod_time = os.path.getmtime(file_being_watched)
            
            if current_mod_time > last_mod_time:
                # File has been modified
                last_mod_time = current_mod_time
                
                # Run compiler with current GUI input if it exists
                result = compile_and_run(
                    file_being_watched,
                    input_from_gui ['input'] if input_from_gui and haskey(input_from_gui, 'input') else ""
                )
                
                # Send result to GUI
                await to_gui.send(json.dumps(result))
                
            await asyncio.sleep(0.02)  # Check every 20ms
            
        except Exception as e:
            print(f"Error in file_watcher coroutine: {e}")
            await asyncio.sleep(0.02)  # Continue checking even if there's an error

async def repl():
    # Start the websocket servers
    async with \
        websockets.serve(handle_to_gui, "localhost", 8765), \
        websockets.serve(handle_from_gui, "localhost", 8766):
        
        # Create tasks for GUI and file watcher
        gui_task = asyncio.create_task(gui())
        watcher_task = asyncio.create_task(file_watcher())
        
        # Keep the servers running
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(repl())
