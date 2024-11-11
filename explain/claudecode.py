"""
Write Python code that has a main routine called `repl`.
Repl creates two websockets called `to_gui` and `from_gui`, at 'ws://localhost:8765' and 'ws://localhost:8766' respectively.
There are 2 coroutines called `gui` and `file_watcher`, respectively.
The code imports the function `compile_and_run` from Python module `compile_and_run.py`.
The function `compile_and_run` takes 2 parameters. The first is a string which is the name of the file being watched. The second is a string derived from `from_gui.input`.
The function `compile_and_run` returns a dict.
The coroutine `gui` waits for JSON input from the `from_gui` websocket, then saves the parsed input into a global variable called `input_from_gui`, and, if the last character of input_from_gui.input is a newline, it calls `compile_and_run` and sends the resulting dict, as a single JSON object, to the `to_gui` websocket.
The coroutine `file_watcher` checks the modification time of the file `test.drawio` every 0.02 seconds. When the file is modified, `file_watcher` calls  `compile_and_run` and sends the resulting dict, as a single JSON object, to the `to_gui` websocket.
"""

import asyncio
import json
import os
import websockets
from compile_and_run import compile_and_run

input_from_gui = None
last_modified_time = None

async def gui(to_gui, from_gui):
    global input_from_gui
    while True:
        try:
            message = await from_gui.recv()
            input_from_gui = json.loads(message)
            
            if input_from_gui['input'].endswith('\n'):
                result = compile_and_run('test.drawio', input_from_gui['input'])
                await to_gui.send(json.dumps(result))
        except websockets.exceptions.ConnectionClosed:
            break
        except Exception as e:
            print(f"Error in gui coroutine: {e}")

async def file_watcher(to_gui):
    global last_modified_time
    while True:
        try:
            current_modified_time = os.path.getmtime('test.drawio')
            
            if last_modified_time is None:
                last_modified_time = current_modified_time
            elif current_modified_time != last_modified_time:
                last_modified_time = current_modified_time
                result = compile_and_run('test.drawio', 
                                       input_from_gui['input'] if input_from_gui else '')
                await to_gui.send(json.dumps(result))
                
            await asyncio.sleep(0.02)
        except Exception as e:
            print(f"Error in file_watcher coroutine: {e}")
            await asyncio.sleep(0.02)

async def repl():
    to_gui = await websockets.connect('ws://localhost:8765')
    from_gui = await websockets.connect('ws://localhost:8766')
    
    try:
        await asyncio.gather(
            gui(to_gui, from_gui),
            file_watcher(to_gui)
        )
    finally:
        await to_gui.close()
        await from_gui.close()

if __name__ == "__main__":
    asyncio.run(repl())

######
######
######
"""
Write Python code that has a main routine called `repl`.
Repl creates two websockets called `to_gui` and `from_gui`, at 'ws://localhost:8765' and 'ws://localhost:8766' respectively.
There are 2 coroutines called `gui` and `file_watcher`, respectively.
A global variable, the file being watched, called `file_being_watched`, is set to `test.drawio`.
The code imports the function `compile_and_run` from Python module `compile_and_run.py`.
The function `compile_and_run` takes 2 parameters. The first is a string which is the name of the file being watched. The second is a string derived from `from_gui.input` if `from_gui.input` exists else the empty string.
The function `compile_and_run` returns a dict.
The coroutine `gui` waits for JSON input from the `from_gui` websocket, then saves the parsed input into a global variable called `input_from_gui`, and, if input_from_gui.input exists and if the last character of input_from_gui.input is a newline, it calls `compile_and_run` and sends the resulting dict, as a single JSON object, to the `to_gui` websocket.
The coroutine `file_watcher` checks the modification time of the file `test.drawio` every 0.02 seconds. When the file is modified, `file_watcher` calls  `compile_and_run` and sends the resulting dict, as a single JSON object, to the `to_gui` websocket.
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
last_modified_time = 0

async def gui(to_gui, from_gui):
    """Coroutine to handle GUI websocket communication"""
    global input_from_gui
    
    async for message in from_gui:
        # Parse incoming JSON message
        input_from_gui = json.loads(message)
        
        # Check if input exists and ends with newline
        if hasattr(input_from_gui, 'input') and input_from_gui.input.endswith('\n'):
            # Call compile_and_run with file name and input
            result = compile_and_run(file_being_watched, input_from_gui.input)
            
            # Send result back to GUI
            await to_gui.send(json.dumps(result))

async def file_watcher(to_gui):
    """Coroutine to watch for file modifications"""
    global last_modified_time
    
    while True:
        try:
            current_modified_time = os.path.getmtime(file_being_watched)
            
            if current_modified_time > last_modified_time:
                # File has been modified
                last_modified_time = current_modified_time
                
                # Call compile_and_run with file name and empty input
                result = compile_and_run(file_being_watched, "")
                
                # Send result back to GUI
                await to_gui.send(json.dumps(result))
                
        except FileNotFoundError:
            print(f"Warning: {file_being_watched} not found")
            
        # Check every 0.02 seconds
        await asyncio.sleep(0.02)

async def repl():
    """Main REPL routine"""
    global last_modified_time
    
    # Initialize last_modified_time
    try:
        last_modified_time = os.path.getmtime(file_being_watched)
    except FileNotFoundError:
        last_modified_time = 0
        print(f"Warning: {file_being_watched} not found")
    
    # Create websocket connections
    async with websockets.serve(lambda ws: None, "localhost", 8765) as to_gui, \
               websockets.serve(lambda ws: None, "localhost", 8766) as from_gui:
        
        # Start coroutines
        await asyncio.gather(
            gui(to_gui, from_gui),
            file_watcher(to_gui)
        )

if __name__ == "__main__":
    asyncio.run(repl())
######
######
######
"""
Write Python code that has a main routine called `repl`.
Repl creates two websockets called `to_gui` and `from_gui`, at 'ws://localhost:8765' and 'ws://localhost:8766' respectively.
There are 2 coroutines called `gui` and `file_watcher`, respectively.
A global variable, the file being watched, called `file_being_watched`, is set to `test.drawio`.
The code imports the function `compile_and_run` from Python module `compile_and_run.py`.
The function `compile_and_run` takes 2 parameters. The first is a string which is the name of the file being watched. The second is a string derived from `from_gui.input` if `from_gui.input` exists else the empty string.
The function `compile_and_run` returns a dict.
The coroutine `gui` waits for JSON input from the `from_gui` websocket, then saves the parsed input into a global variable called `input_from_gui`, and, if input_from_gui.input exists and if the last character of input_from_gui.input is a newline, it calls `compile_and_run` and sends the resulting dict, as a single JSON object, to the `to_gui` websocket.
The coroutine `file_watcher` checks the modification time of the file `test.drawio` every 0.02 seconds. When the file is modified, `file_watcher` calls  `compile_and_run` and sends the resulting dict, as a single JSON object, to the `to_gui` websocket.
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
last_modified_time = 0

async def gui(to_gui, from_gui):
    """Coroutine to handle GUI websocket communication"""
    global input_from_gui
    
    async for message in from_gui:
        # Parse incoming JSON message
        input_from_gui = json.loads(message)
        
        # Check if input exists and ends with newline
        if hasattr(input_from_gui, 'input') and input_from_gui.input.endswith('\n'):
            # Call compile_and_run with file name and input
            result = compile_and_run(file_being_watched, input_from_gui.input)
            
            # Send result back to GUI
            await to_gui.send(json.dumps(result))

async def file_watcher(to_gui):
    """Coroutine to watch for file modifications"""
    global last_modified_time
    
    while True:
        try:
            current_modified_time = os.path.getmtime(file_being_watched)
            
            if current_modified_time > last_modified_time:
                # File has been modified
                last_modified_time = current_modified_time
                
                # Call compile_and_run with file name and empty input
                result = compile_and_run(file_being_watched, "")
                
                # Send result back to GUI
                await to_gui.send(json.dumps(result))
                
        except FileNotFoundError:
            print(f"Warning: {file_being_watched} not found")
            
        # Check every 0.02 seconds
        await asyncio.sleep(0.02)

async def repl():
    """Main REPL routine"""
    global last_modified_time
    
    # Initialize last_modified_time
    try:
        last_modified_time = os.path.getmtime(file_being_watched)
    except FileNotFoundError:
        last_modified_time = 0
        print(f"Warning: {file_being_watched} not found")
    
    # Create websocket connections
    async with websockets.serve(lambda ws: None, "localhost", 8765) as to_gui, \
               websockets.serve(lambda ws: None, "localhost", 8766) as from_gui:
        
        # Start coroutines
        await asyncio.gather(
            gui(to_gui, from_gui),
            file_watcher(to_gui)
        )

if __name__ == "__main__":
    asyncio.run(repl())
######
######
######

"""
Write Python code that has a main routine called `repl`.
Repl creates two websockets called `to_gui` and `from_gui`, at 'ws://localhost:8765' and 'ws://localhost:8766' respectively.
There are 2 coroutines called `gui` and `file_watcher`, respectively.
A global variable, the file being watched, called `file_being_watched`, is set to `test.drawio`.
The code imports the function `compile_and_run` from Python module `compile_and_run.py`.
The function `compile_and_run` takes 2 parameters. The first is a string which is the name of the file being watched. The second is a string derived from `from_gui.input` if `from_gui.input` exists else the empty string.
The function `compile_and_run` returns a dict.
The coroutine `gui` waits for JSON input from the `from_gui` websocket, then saves the parsed input into a global variable called `input_from_gui`, and, if input_from_gui.input exists and if the last character of input_from_gui.input is a newline, it calls `compile_and_run` with appropriate parameters, as above, and sends the resulting dict, as a single JSON object, to the `to_gui` websocket.
The coroutine `file_watcher` checks the modification time of the file `test.drawio` every 0.02 seconds. When the file is modified, `file_watcher` calls  `compile_and_run` with appropriate parameters as above  and sends the resulting dict, as a single JSON object, to the `to_gui` websocket.
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
last_modified_time = 0

async def gui(to_gui, from_gui):
    global input_from_gui
    
    while True:
        try:
            # Wait for input from GUI
            message = await from_gui.recv()
            input_from_gui = json.loads(message)
            
            # Check if input exists and ends with newline
            if hasattr(input_from_gui, 'input') and input_from_gui.input.endswith('\n'):
                # Call compile_and_run with appropriate parameters
                result = compile_and_run(file_being_watched, input_from_gui.input)
                
                # Send result to GUI
                await to_gui.send(json.dumps(result))
                
        except websockets.exceptions.ConnectionClosed:
            break
        except Exception as e:
            print(f"Error in gui coroutine: {e}")

async def file_watcher(to_gui):
    global last_modified_time
    
    while True:
        try:
            current_modified_time = os.path.getmtime(file_being_watched)
            
            if current_modified_time > last_modified_time:
                # File has been modified
                last_modified_time = current_modified_time
                
                # Get input string from input_from_gui if it exists
                input_string = ""
                if input_from_gui and hasattr(input_from_gui, 'input'):
                    input_string = input_from_gui.input
                
                # Call compile_and_run
                result = compile_and_run(file_being_watched, input_string)
                
                # Send result to GUI
                await to_gui.send(json.dumps(result))
            
            # Wait before checking again
            await asyncio.sleep(0.02)
            
        except Exception as e:
            print(f"Error in file_watcher coroutine: {e}")
            await asyncio.sleep(0.02)

async def repl():
    # Create websocket servers
    to_gui = await websockets.serve(lambda ws, path: None, "localhost", 8765)
    from_gui = await websockets.serve(lambda ws, path: None, "localhost", 8766)
    
    # Get the first (and only) websocket for each server
    to_gui_ws = to_gui.ws_server.websockets.pop()
    from_gui_ws = from_gui.ws_server.websockets.pop()
    
    # Start coroutines
    await asyncio.gather(
        gui(to_gui_ws, from_gui_ws),
        file_watcher(to_gui_ws)
    )

if __name__ == "__main__":
    asyncio.run(repl())

######
######
######

"""
This program implements a REPL system with the following components:
- Two websockets for GUI communication (to_gui and from_gui) on localhost ports 8765/8766
- A file watcher monitoring test.drawio for modifications
- A GUI coroutine handling websocket input/output
- Integration with compile_and_run function from external module
- JSON-based communication between components
The system responds to both file modifications and GUI input by compiling/running
and sending results back to the GUI via websocket.
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

async def gui(to_gui, from_gui):
    global input_from_gui
    
    async for message in from_gui:
        # Parse incoming JSON message
        input_from_gui = json.loads(message)
        
        # Check if input exists and ends with newline
        if hasattr(input_from_gui, 'input') and input_from_gui.input.endswith('\n'):
            # Call compile_and_run with appropriate parameters
            result = compile_and_run(
                file_being_watched,
                input_from_gui.input if hasattr(input_from_gui, 'input') else ""
            )
            
            # Send result back to GUI
            await to_gui.send(json.dumps(result))

async def file_watcher(to_gui):
    last_modified_time = 0
    
    while True:
        try:
            current_modified_time = os.path.getmtime(file_being_watched)
            
            if current_modified_time > last_modified_time:
                # File was modified, call compile_and_run
                result = compile_and_run(
                    file_being_watched,
                    input_from_gui.input if input_from_gui and hasattr(input_from_gui, 'input') else ""
                )
                
                # Send result back to GUI
                await to_gui.send(json.dumps(result))
                
                last_modified_time = current_modified_time
                
        except FileNotFoundError:
            print(f"Warning: {file_being_watched} not found")
            
        await asyncio.sleep(0.02)  # Check every 20ms

async def repl():
    async with websockets.serve(lambda ws: None, "localhost", 8765) as to_gui, \
               websockets.serve(lambda ws: None, "localhost", 8766) as from_gui:
        
        # Start both coroutines
        await asyncio.gather(
            gui(to_gui, from_gui),
            file_watcher(to_gui)
        )

if __name__ == "__main__":
    asyncio.run(repl())

######
######
###### 5 ######
"""
This program implements a REPL system with the following components:
- Two websockets for GUI communication (to_gui and from_gui)
- A file watcher coroutine monitoring test.drawio for changes
- A GUI coroutine handling WebSocket input/output
- Integration with compile_and_run function for processing
- Main REPL routine coordinating all components
The system watches for file changes and GUI input, processes them through
compile_and_run, and sends results back to the GUI via WebSocket.
"""

import asyncio
import json
import os
import websockets
from compile_and_run import compile_and_run

# Global variables
file_being_watched = "test.drawio"
input_from_gui = None
last_mod_time = 0

async def gui(to_gui, from_gui):
    """Coroutine handling GUI WebSocket communication"""
    global input_from_gui
    
    try:
        while True:
            # Wait for input from GUI WebSocket
            message = await from_gui.recv()
            input_from_gui = json.loads(message)
            
            # Process input if it exists and ends with newline
            if (hasattr(input_from_gui, 'input') and 
                input_from_gui.input and 
                input_from_gui.input[-1] == '\n'):
                
                result = compile_and_run(
                    file_being_watched,
                    input_from_gui.input if hasattr(input_from_gui, 'input') else ""
                )
                
                # Send result back to GUI
                await to_gui.send(json.dumps(result))
                
    except websockets.exceptions.ConnectionClosed:
        print("GUI WebSocket connection closed")

async def file_watcher(to_gui):
    """Coroutine monitoring file changes"""
    global last_mod_time
    
    while True:
        try:
            current_mod_time = os.path.getmtime(file_being_watched)
            
            if current_mod_time > last_mod_time:
                last_mod_time = current_mod_time
                
                # Process file change
                result = compile_and_run(
                    file_being_watched,
                    input_from_gui.input if (input_from_gui and hasattr(input_from_gui, 'input')) else ""
                )
                
                # Send result back to GUI
                await to_gui.send(json.dumps(result))
                
        except FileNotFoundError:
            print(f"File {file_being_watched} not found")
            
        await asyncio.sleep(0.02)  # Check every 20ms

async def repl():
    """Main REPL routine"""
    # Set up WebSocket connections
    to_gui = await websockets.connect('ws://localhost:8765')
    from_gui = await websockets.connect('ws://localhost:8766')
    
    try:
        # Create tasks for GUI and file watcher
        gui_task = asyncio.create_task(gui(to_gui, from_gui))
        watcher_task = asyncio.create_task(file_watcher(to_gui))
        
        # Wait for both tasks
        await asyncio.gather(gui_task, watcher_task)
        
    finally:
        # Clean up WebSocket connections
        await to_gui.close()
        await from_gui.close()

if __name__ == "__main__":
    asyncio.run(repl())

######
######
###### 6 ######

"""
This program implements a REPL system with the following components:
- Two websockets: to_gui (8765) and from_gui (8766)
- A GUI coroutine that handles websocket input/output
- A file watcher coroutine that monitors test.drawio
- Both coroutines use compile_and_run to process input and send results as JSON
- The system responds to both file changes and GUI input
"""

import asyncio
import json
import os
import websockets
import time
from compile_and_run import compile_and_run

# Global variables
file_being_watched = "test.drawio"
input_from_gui = None
to_gui_connections = set()
from_gui_connections = set()

async def handle_to_gui(websocket):
    to_gui_connections.add(websocket)
    try:
        await websocket.wait_closed()
    finally:
        to_gui_connections.remove(websocket)

async def handle_from_gui(websocket):
    from_gui_connections.add(websocket)
    try:
        await websocket.wait_closed()
    finally:
        from_gui_connections.remove(websocket)

async def gui():
    global input_from_gui
    
    while True:
        if from_gui_connections:
            websocket = next(iter(from_gui_connections))
            try:
                # Wait for input from the GUI websocket
                message = await websocket.recv()
                input_from_gui = json.loads(message)
                
                # Check if input exists and ends with newline
                if hasattr(input_from_gui, 'input') and input_from_gui.input.endswith('\n'):
                    # Call compile_and_run with appropriate parameters
                    result = compile_and_run(
                        file_being_watched,
                        input_from_gui.input if hasattr(input_from_gui, 'input') else ""
                    )
                    
                    # Send result to all connected GUI clients
                    for to_gui in to_gui_connections:
                        await to_gui.send(json.dumps(result))
                    
            except websockets.exceptions.ConnectionClosed:
                continue
            except Exception as e:
                print(f"Error in GUI coroutine: {e}")
        await asyncio.sleep(0.01)

async def file_watcher():
    last_modified = 0
    
    while True:
        try:
            current_modified = os.path.getmtime(file_being_watched)
            
            if current_modified > last_modified:
                # File has been modified, call compile_and_run
                result = compile_and_run(
                    file_being_watched,
                    input_from_gui.input if input_from_gui and hasattr(input_from_gui, 'input') else ""
                )
                
                # Send result to all connected GUI clients
                for to_gui in to_gui_connections:
                    await to_gui.send(json.dumps(result))
                last_modified = current_modified
            
            # Check every 0.02 seconds
            await asyncio.sleep(0.02)
            
        except Exception as e:
            print(f"Error in file watcher coroutine: {e}")
            await asyncio.sleep(0.02)

async def repl():
    # Start websocket servers
    to_gui_server = await websockets.serve(handle_to_gui, 'localhost', 8765)
    from_gui_server = await websockets.serve(handle_from_gui, 'localhost', 8766)
    
    # Create tasks for GUI and file watcher coroutines
    gui_task = asyncio.create_task(gui())
    watcher_task = asyncio.create_task(file_watcher())
    
    # Wait for both tasks to complete
    await asyncio.gather(gui_task, watcher_task)
    
    # Cleanup
    to_gui_server.close()
    from_gui_server.close()
    await to_gui_server.wait_closed()
    await from_gui_server.wait_closed()

if __name__ == "__main__":
    asyncio.run(repl())

######
######
###### 7 ######

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

async def gui(to_gui, from_gui):
    global input_from_gui
    
    while True:
        try:
            # Wait for input from GUI
            message = await from_gui.recv()
            input_from_gui = json.loads(message)
            
            # Check if input exists and ends with newline
            if hasattr(input_from_gui, 'input') and input_from_gui.input.endswith('\n'):
                # Run compiler with input from GUI
                result = compile_and_run(
                    file_being_watched,
                    input_from_gui.input if hasattr(input_from_gui, 'input') else ""
                )
                
                # Send result back to GUI
                await to_gui.send(json.dumps(result))
                
        except websockets.exceptions.ConnectionClosed:
            break
        except Exception as e:
            print(f"Error in gui coroutine: {e}")
            
async def file_watcher(to_gui):
    global last_mod_time
    
    while True:
        try:
            current_mod_time = os.path.getmtime(file_being_watched)
            
            if current_mod_time > last_mod_time:
                # File has been modified
                last_mod_time = current_mod_time
                
                # Run compiler with current GUI input if it exists
                result = compile_and_run(
                    file_being_watched,
                    input_from_gui.input if input_from_gui and hasattr(input_from_gui, 'input') else ""
                )
                
                # Send result back to GUI
                await to_gui.send(json.dumps(result))
                
            await asyncio.sleep(0.02)  # Check every 20ms
            
        except Exception as e:
            print(f"Error in file_watcher coroutine: {e}")
            await asyncio.sleep(0.02)  # Continue checking even if there's an error

async def repl():
    async with websockets.serve(lambda ws: None, "localhost", 8765) as to_gui, \
               websockets.serve(lambda ws: None, "localhost", 8766) as from_gui:
        
        # Create tasks for GUI and file watcher
        gui_task = asyncio.create_task(gui(to_gui, from_gui))
        watcher_task = asyncio.create_task(file_watcher(to_gui))
        
        # Wait for both tasks to complete
        await asyncio.gather(gui_task, watcher_task)

if __name__ == "__main__":
    asyncio.run(repl())

    ######
######
###### 7a ######

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
connected_clients = set()

async def handle_client(websocket):
    connected_clients.add(websocket)
    try:
        await websocket.wait_closed()
    finally:
        connected_clients.remove(websocket)

async def broadcast_to_gui(message):
    if connected_clients:
        await asyncio.gather(
            *[client.send(message) for client in connected_clients]
        )

async def gui(websocket):
    global input_from_gui
    
    while True:
        try:
            # Wait for input from GUI
            message = await websocket.recv()
            input_from_gui = json.loads(message)
            
            # Check if input exists and ends with newline
            if hasattr(input_from_gui, 'input') and input_from_gui.input.endswith('\n'):
                # Run compiler with input from GUI
                result = compile_and_run(
                    file_being_watched,
                    input_from_gui.input if hasattr(input_from_gui, 'input') else ""
                )
                
                # Broadcast result to all connected clients
                await broadcast_to_gui(json.dumps(result))
                
        except websockets.exceptions.ConnectionClosed:
            break
        except Exception as e:
            print(f"Error in gui coroutine: {e}")

async def file_watcher():
    global last_mod_time
    
    while True:
        try:
            current_mod_time = os.path.getmtime(file_being_watched)
            
            if current_mod_time > last_mod_time:
                # File has been modified
                last_mod_time = current_mod_time
                
                # Run compiler with current GUI input if it exists
                result = compile_and_run(
                    file_being_watched,
                    input_from_gui.input if input_from_gui and hasattr(input_from_gui, 'input') else ""
                )
                
                # Broadcast result to all connected clients
                await broadcast_to_gui(json.dumps(result))
                
            await asyncio.sleep(0.02)  # Check every 20ms
            
        except Exception as e:
            print(f"Error in file_watcher coroutine: {e}")
            await asyncio.sleep(0.02)  # Continue checking even if there's an error

async def repl():
    # Start the file watcher
    watcher_task = asyncio.create_task(file_watcher())
    
    # Start both websocket servers
    async with \
        websockets.serve(handle_client, "localhost", 8765) as to_gui_server, \
        websockets.serve(gui, "localhost", 8766) as from_gui_server:
        
        # Run indefinitely
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(repl())

### 7b

// In GUI client
const to_gui = new WebSocket('ws://localhost:8765');  // For receiving messages
const from_gui = new WebSocket('ws://localhost:8766'); // For sending messages

###
###
### 7c

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

async def handle_from_gui(websocket):
    global from_gui
    from_gui = websocket
    await websocket.wait_closed()
    from_gui = None

async def handle_to_gui(websocket):
    global to_gui
    to_gui = websocket
    await websocket.wait_closed()
    to_gui = None

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
            
            # Check if input exists and ends with newline
            if to_gui and hasattr(input_from_gui, 'input') and input_from_gui.input.endswith('\n'):
                # Run compiler with input from GUI
                result = compile_and_run(
                    file_being_watched,
                    input_from_gui.input if hasattr(input_from_gui, 'input') else ""
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
                    input_from_gui.input if input_from_gui and hasattr(input_from_gui, 'input') else ""
                )
                
                # Send result to GUI
                await to_gui.send(json.dumps(result))
                
            await asyncio.sleep(0.02)  # Check every 20ms
            
        except Exception as e:
            print(f"Error in file_watcher coroutine: {e}")
            await asyncio.sleep(0.02)  # Continue checking even if there's an error

async def repl():
    # Start the websocket servers
    to_gui_server = await websockets.serve(handle_to_gui, "localhost", 8765)
    from_gui_server = await websockets.serve(handle_from_gui, "localhost", 8766)
    
    # Create tasks for GUI and file watcher
    gui_task = asyncio.create_task(gui())
    watcher_task = asyncio.create_task(file_watcher())
    
    try:
        # Keep the servers running
        await asyncio.gather(
            to_gui_server.wait_closed(),
            from_gui_server.wait_closed(),
            gui_task,
            watcher_task
        )
    finally:
        # Clean up
        to_gui_server.close()
        from_gui_server.close()
        await to_gui_server.wait_closed()
        await from_gui_server.wait_closed()

if __name__ == "__main__":
    asyncio.run(repl())

###
###
### 7d





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

async def handle_from_gui(websocket):
    global from_gui
    from_gui = websocket
    await websocket.wait_closed()
    from_gui = None

async def handle_to_gui(websocket):
    global to_gui
    to_gui = websocket
    await websocket.wait_closed()
    to_gui = None

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
            
            # Check if input exists and ends with newline
            if to_gui and hasattr(input_from_gui, 'input') and input_from_gui.input.endswith('\n'):
                # Run compiler with input from GUI
                result = compile_and_run(
                    file_being_watched,
                    input_from_gui.input if hasattr(input_from_gui, 'input') else ""
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
                    input_from_gui.input if input_from_gui and hasattr(input_from_gui, 'input') else ""
                )
                
                # Send result to GUI
                await to_gui.send(json.dumps(result))
                
            await asyncio.sleep(0.02)  # Check every 20ms
            
        except Exception as e:
            print(f"Error in file_watcher coroutine: {e}")
            await asyncio.sleep(0.02)  # Continue checking even if there's an error

async def repl():
    # Start the websocket servers
    to_gui_server = await websockets.serve(handle_to_gui, "localhost", 8765)
    from_gui_server = await websockets.serve(handle_from_gui, "localhost", 8766)
    
    # Create tasks for GUI and file watcher
    gui_task = asyncio.create_task(gui())
    watcher_task = asyncio.create_task(file_watcher())
    
    try:
        # Keep the servers running
        await asyncio.gather(
            to_gui_server.wait_closed(),
            from_gui_server.wait_closed(),
            gui_task,
            watcher_task
        )
    finally:
        # Clean up
        to_gui_server.close()
        from_gui_server.close()
        await to_gui_server.wait_closed()
        await from_gui_server.wait_closed()

if __name__ == "__main__":
    asyncio.run(repl())

###
###
###
    

