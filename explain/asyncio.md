At a low level, `asyncio` is a Python library designed for asynchronous programming, allowing developers to write concurrent code that handles many tasks (e.g., I/O-bound operations) in a single-threaded environment. It is based on the **event loop**, a core structure that manages scheduling and running multiple asynchronous tasks without creating additional threads or processes.

### Core Concepts and Components of `asyncio`

1. **Event Loop**:
   - The **event loop** is the heart of `asyncio`. It is a loop that continually checks for tasks that are ready to run, executes them, and handles I/O events.
   - The loop iterates repeatedly, waiting for I/O events (e.g., data on a network socket, a file read to complete), and when an event is ready, it triggers the associated callback or coroutine.
   - Only one task executes at a time on a single thread, but the event loop allows switching between tasks in an efficient, non-blocking way, making it well-suited for handling many I/O-bound tasks concurrently.
   
   ```python
   loop = asyncio.get_event_loop()
   loop.run_until_complete(main())
   ```

2. **Coroutines**:
   - Coroutines are **special functions** defined with `async def` that allow suspension and resumption at specific points using `await`. These are the building blocks for `asyncio`.
   - When a coroutine calls `await`, it yields control back to the event loop, allowing other tasks to run while waiting for the awaited operation to complete.

   ```python
   async def example_coroutine():
       await asyncio.sleep(1)  # Yield control back to the event loop
       print("Coroutine finished")
   ```

3. **Tasks**:
   - A `Task` in `asyncio` is a wrapper for a coroutine, allowing it to be scheduled and executed by the event loop.
   - The event loop keeps track of all active tasks, running them one by one until completion or until they reach a point where they must await something (like an I/O operation).
   - Tasks are created with `asyncio.create_task(coroutine())` or directly with `loop.create_task`.

   ```python
   task = asyncio.create_task(example_coroutine())
   await task  # Wait for task to complete
   ```

4. **Future Objects**:
   - An `asyncio.Future` is a **placeholder** for data that isn’t yet available but will be at some point.
   - Futures are used internally by `asyncio` to manage results of tasks and ensure tasks have completed before accessing their results.
   - Futures can also be used directly for more control, such as setting a result when a callback finishes an operation.

   ```python
   future = asyncio.Future()
   future.set_result("Data ready")
   await future  # Waits for the future to have a result
   ```

5. **Awaitables**:
   - `asyncio` handles **awaitables**, which are objects you can await using `await`. The main types of awaitables are coroutines, tasks, and futures.
   - `await` suspends execution of the coroutine until the awaitable completes.

   ```python
   await asyncio.sleep(1)  # Awaiting an asyncio sleep coroutine
   ```

6. **Scheduling and Cooperative Multitasking**:
   - `asyncio` achieves concurrency by **scheduling tasks** in a cooperative multitasking style, meaning each task voluntarily gives up control by using `await`.
   - While one task is waiting on I/O (like a network request or file read), the event loop can schedule and execute other tasks that are ready.
   - The event loop cycles through tasks, switching between them at `await` points. This allows for multiple tasks to run concurrently without preemption (as seen in multithreaded environments).

### Low-Level Working of `asyncio`

1. **Registration of Tasks**:
   - When you create a task or schedule a coroutine, it is registered with the event loop. The event loop adds this task to its internal list of active tasks.

2. **Handling I/O and Blocking Points**:
   - When a task reaches an `await` on an I/O operation (like `await asyncio.sleep()` or `await websocket.recv()`), it tells the event loop that it cannot proceed until this I/O is complete.
   - The event loop marks this task as "waiting" and will only resume it when the awaited operation completes.

3. **Polling and Callbacks**:
   - The event loop uses low-level **polling mechanisms** (e.g., `select` or `epoll` on Unix, `IOCP` on Windows) to detect when I/O operations are ready.
   - When I/O completes, a callback (internal function) is triggered, which "wakes up" the coroutine that was awaiting this I/O operation.

4. **Resuming Tasks**:
   - The event loop places the "ready" task back in its queue of active tasks and continues running it until it either completes or reaches another `await` point.
   - This cycle of suspending and resuming tasks allows the event loop to interleave I/O-bound operations with other tasks.

5. **Error Handling**:
   - Errors within a coroutine propagate through the task, and the event loop can handle these exceptions if the task wasn’t directly awaited.
   - If a task fails, it is marked as "done" with an error result, which can be checked or handled by other coroutines or tasks.

### Example of Low-Level `asyncio` Code with `Future` and `Event Loop`

Below is a simple example using `asyncio`'s low-level constructs to demonstrate how tasks, futures, and the event loop work together.

```python
import asyncio

async def background_task(future):
    await asyncio.sleep(2)  # Simulate an I/O operation
    future.set_result("Task completed")  # Set result in the future

async def main():
    loop = asyncio.get_running_loop()
    
    # Create a Future object and a background task to complete it
    future = loop.create_future()
    loop.create_task(background_task(future))

    print("Waiting for the background task to finish...")
    result = await future  # Wait for the future to have a result
    print(result)

asyncio.run(main())
```

In this example:
- A `Future` object is created.
- A task (`background_task`) simulates a delay, then sets a result on the future.
- The main coroutine `await`s the future, so it suspends until the future is marked as complete.

### Summary

`asyncio` provides a low-level mechanism for handling concurrency without threads or processes. Its core principles include:
- **Event loop** that runs in a single thread and manages task scheduling.
- **Coroutines** that yield control using `await` to allow the event loop to schedule other tasks.
- **Futures and Tasks** to manage the results of coroutines.
- **Cooperative multitasking** where tasks voluntarily yield control, enabling efficient concurrency for I/O-bound programs. 

This architecture allows Python to handle many I/O-bound operations concurrently, making `asyncio` ideal for web servers, network applications, and similar use cases where managing multiple connections or file operations is essential.

# Coroutines vs. Tasks
In Python's `asyncio`, **coroutines** and **tasks** are related but serve different roles in asynchronous programming. Here’s a breakdown of the distinctions:

### 1. **Coroutines**:
   - **Definition**: A **coroutine** is a function that you define using `async def`. It is the basic building block of asynchronous code in Python. 
   - **Execution**: When you call a coroutine function, it doesn't start executing immediately; instead, it returns a coroutine object. To execute the coroutine, you need to await it (e.g., `await my_coroutine()`).
   - **Purpose**: Coroutines allow you to write asynchronous code that can be suspended and resumed at certain points (using `await`).
   - **Example**:
     ```python
     async def my_coroutine():
         print("Starting coroutine")
         await asyncio.sleep(1)
         print("Coroutine done")
     ```
   - **Direct Usage**: Coroutines are generally meant to be awaited directly or wrapped in tasks if they need to be scheduled immediately.

### 2. **Tasks**:
   - **Definition**: A **task** is a wrapper around a coroutine that runs it in the background as part of the `asyncio` event loop. Tasks are created by passing a coroutine to `asyncio.create_task()` or `loop.create_task()`.
   - **Execution**: Unlike coroutines, tasks start executing immediately when they’re created, allowing them to run concurrently with other tasks. This means you don’t have to `await` a task right after creating it.
   - **Purpose**: Tasks are useful when you want a coroutine to run "in the background" while your program continues doing other things.
   - **Example**:
     ```python
     async def main():
         task = asyncio.create_task(my_coroutine())  # Starts executing immediately
         print("Task created and running in the background")
         await task  # Wait for the task to finish

     asyncio.run(main())
     ```
   - **Concurrency**: Tasks allow multiple coroutines to run concurrently without directly waiting for each to complete.

### Key Differences

| Aspect                | Coroutine                                         | Task                                           |
|-----------------------|---------------------------------------------------|------------------------------------------------|
| **Creation**          | Created by calling a function defined with `async def`, like `my_coroutine()` | Created by wrapping a coroutine in `asyncio.create_task()`, like `asyncio.create_task(my_coroutine())` |
| **Execution**         | Returns a coroutine object when called; doesn’t start until awaited | Starts executing immediately after creation |
| **Control**           | Must be awaited to run to completion | Can run concurrently with other tasks without awaiting |
| **Usage**             | For defining asynchronous behavior | For scheduling coroutines to run concurrently |
| **Concurrent Execution** | Does not run concurrently unless turned into a task or awaited in parallel with others | Runs concurrently with other tasks in the event loop |

### Example: Coroutine vs. Task in Practice

Consider an example where we want to run two instances of a coroutine concurrently:

```python
import asyncio

async def my_coroutine(name):
    print(f"{name} started")
    await asyncio.sleep(2)  # Simulates a long I/O operation
    print(f"{name} finished")

# Using coroutines directly - they run sequentially if awaited directly
async def run_sequentially():
    await my_coroutine("Coroutine 1")
    await my_coroutine("Coroutine 2")

# Using tasks - they run concurrently
async def run_concurrently():
    task1 = asyncio.create_task(my_coroutine("Task 1"))
    task2 = asyncio.create_task(my_coroutine("Task 2"))
    await task1
    await task2

async def main():
    print("Running coroutines sequentially:")
    await run_sequentially()
    print("\nRunning tasks concurrently:")
    await run_concurrently()

asyncio.run(main())
```

**Output:**
```
Running coroutines sequentially:
Coroutine 1 started
Coroutine 1 finished
Coroutine 2 started
Coroutine 2 finished

Running tasks concurrently:
Task 1 started
Task 2 started
Task 1 finished
Task 2 finished
```

- In `run_sequentially`, the two coroutines run one after the other because they are awaited in sequence.
- In `run_concurrently`, the two coroutines run concurrently because they are wrapped in tasks, which start running as soon as they are created.

### Summary

- **Coroutines**: Define asynchronous operations and require `await` to execute them.
- **Tasks**: Run coroutines concurrently in the event loop without needing to be awaited immediately, making them ideal for background processing.

# Websockets
To work with WebSockets at a low level in Python, you generally need to use libraries like `websockets`, which provides a convenient API for establishing and managing WebSocket connections. However, understanding how WebSockets work at a low level can be helpful, as they operate on top of the basic **TCP protocol** and involve specific **handshakes** and **message frames** to maintain a continuous, bidirectional connection between a client and a server.

Here’s a look at both how WebSockets function under the hood and how to use them in Python with `websockets`.

### Low-Level Basics of WebSockets

1. **Protocol**: 
   - WebSockets are an upgrade to the traditional HTTP connection that enables continuous, bidirectional communication. This allows a client and server to keep a connection open and exchange messages back and forth without needing to repeatedly request a connection.
   - They use TCP at the transport layer but add a WebSocket protocol layer that manages the handshake and message framing.

2. **Handshake**:
   - The WebSocket connection starts with an HTTP handshake, which is essentially an HTTP GET request that includes special headers to indicate a WebSocket upgrade request.
   - If the server agrees to upgrade, it responds with an HTTP 101 status code ("Switching Protocols"), establishing the WebSocket connection.
   - After this handshake, the connection switches to a raw TCP stream where messages can be sent in both directions.

3. **Message Framing**:
   - WebSocket messages are divided into frames that contain information about whether they are the last frame in a message, the type of data (text or binary), and the payload.
   - The client and server exchange data by writing frames to the TCP socket. Each frame has a specific structure, including an opcode (e.g., text frame or binary frame), masking keys (on the client side), and the payload length.

### Setting Up a WebSocket Server and Client in Python

To implement WebSocket connections in Python, you can use the `websockets` library, which abstracts away much of the low-level details. Here’s how to use it to create a basic WebSocket server and client.

#### Step 1: Install the `websockets` library
If you haven’t already, install the `websockets` library:
```bash
pip install websockets
```

#### Step 2: Create a WebSocket Server

Here's an example of a simple WebSocket server using `asyncio` and `websockets`.

```python
import asyncio
import websockets

# Define the server coroutine
async def server_handler(websocket, path):
    print("Client connected")
    try:
        async for message in websocket:
            print(f"Received message: {message}")
            # Echo the message back to the client
            await websocket.send(f"Echo: {message}")
    except websockets.ConnectionClosed:
        print("Client disconnected")

# Start the server
async def start_server():
    async with websockets.serve(server_handler, "localhost", 8765):
        print("WebSocket server started on ws://localhost:8765")
        await asyncio.Future()  # Run forever

# Run the server
asyncio.run(start_server())
```

- **Explanation**:
  - `websockets.serve(server_handler, "localhost", 8765)`: Starts the WebSocket server at `ws://localhost:8765`.
  - `server_handler`: The handler for client connections, which processes each message from the client and sends a response.
  - `async for message in websocket`: Asynchronously receive messages from the client, allowing other connections to be handled concurrently.

#### Step 3: Create a WebSocket Client

Now, let’s create a client that connects to this server and sends a message.

```python
import asyncio
import websockets

# Define the client coroutine
async def client_handler():
    uri = "ws://localhost:8765"
    async with websockets.connect(uri) as websocket:
        print("Connected to the server")

        # Send a message to the server
        await websocket.send("Hello, Server!")
        print("Message sent to server")

        # Receive the echoed response from the server
        response = await websocket.recv()
        print(f"Received from server: {response}")

# Run the client
asyncio.run(client_handler())
```

- **Explanation**:
  - `websockets.connect(uri)`: Connects to the WebSocket server at the specified URI.
  - `await websocket.send("Hello, Server!")`: Sends a message to the server.
  - `await websocket.recv()`: Waits for a message from the server, then prints the response.

### Key Points to Note

- **Concurrency**: Because `websockets` is built on `asyncio`, both the server and client can handle multiple connections and messages concurrently.
- **Error Handling**: WebSocket connections can drop unexpectedly, so use try-except blocks (particularly around `websocket.recv()` or `websocket.send()`) to handle `ConnectionClosed` exceptions gracefully.
- **Non-blocking I/O**: `asyncio` and `websockets` ensure that I/O operations are non-blocking, so multiple clients can connect and communicate with the server without any performance bottlenecks.

### Example with Periodic Communication

Suppose you want the server to periodically send a message to the client. Here’s how you might extend the server:

```python
import asyncio
import websockets

async def server_handler(websocket, path):
    print("Client connected")
    try:
        # Periodically send a message to the client every 5 seconds
        while True:
            await asyncio.sleep(5)
            await websocket.send("Server message every 5 seconds")
    except websockets.ConnectionClosed:
        print("Client disconnected")

# Start the server
async def start_server():
    async with websockets.serve(server_handler, "localhost", 8765):
        print("WebSocket server started on ws://localhost:8765")
        await asyncio.Future()  # Run forever

asyncio.run(start_server())
```

In this version, the server sends a message to the client every 5 seconds as long as the client stays connected.

### Summary

Using WebSockets at a low level in Python with `asyncio` and `websockets` involves:
- Setting up the **event loop** to manage asynchronous tasks.
- Writing asynchronous functions for both **sending and receiving messages**.
- Managing the **connection lifecycle** by handling connection establishment, message transmission, and disconnection events.
- Working with `websockets.serve` and `websockets.connect` to establish and manage WebSocket connections between clients and servers.

This setup allows Python applications to maintain efficient, real-time, bidirectional communication over a single TCP connection with WebSocket-compatible clients, such as modern web browsers or other networked applications.
# Appendix - Prompt

The above is ChatGPTs answer to the prompt "explain asyncio at a low level".

A second prompt was used "what's the difference between coroutines and tasks?"

"explain how to use websockets in Python at a low level"