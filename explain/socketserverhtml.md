Let's create the HTML and JavaScript code for the client-side, which includes a `textarea` that sends its contents over a WebSocket connection whenever it's changed. We'll also create the Python server-side code to listen for these updates.

### HTML + JavaScript Client

This HTML file includes a `textarea` element and JavaScript that opens a WebSocket connection and sends updates when the content of the `textarea` changes.

Save this as `index.html`:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>WebSocket TextArea</title>
</head>
<body>
    <h1>WebSocket TextArea</h1>
    <textarea id="myTextarea" rows="10" cols="30" placeholder="Type here..."></textarea>

    <script>
        // Open a WebSocket connection to the server
        const socket = new WebSocket('ws://localhost:6789');

        // Get the textarea element
        const textarea = document.getElementById('myTextarea');

        // Listen for changes in the textarea
        textarea.addEventListener('input', () => {
            if (socket.readyState === WebSocket.OPEN) {
                // Send the textarea name and its content as a pair of strings
                const message = JSON.stringify({
                    name: textarea.id,
                    content: textarea.value
                });
                socket.send(message);
            }
        });

        // Handle incoming messages from the server (optional)
        socket.addEventListener('message', (event) => {
            console.log('Received from server:', event.data);
        });

        // Handle connection errors
        socket.addEventListener('error', (error) => {
            console.error('WebSocket error:', error);
        });
    </script>
</body>
</html>
```

### Python WebSocket Server

The Python code below sets up a WebSocket server that listens for incoming messages from the client. When the server receives a message, it prints out the data, which includes the `textarea` name and its contents.

This code uses the `websockets` library, so make sure it's installed:

```bash
pip install websockets
```

Save this as `server.py`:

```python
import asyncio
import websockets
import json

async def handler(websocket, path):
    print("WebSocket connection established.")
    async for message in websocket:
        data = json.loads(message)
        textarea_name = data['name']
        textarea_content = data['content']
        print(f"Received update from {textarea_name}: {textarea_content}")

async def main():
    async with websockets.serve(handler, "localhost", 6789):
        print("Server started on ws://localhost:6789")
        await asyncio.Future()  # Run forever

# Run the server
asyncio.run(main())
```

### Explanation

1. **Client Code (HTML + JavaScript)**:
   - Connects to the WebSocket server at `ws://localhost:6789`.
   - Sends a JSON object with two keys:
     - `name`: The ID of the `textarea` (in this case, `"myTextarea"`).
     - `content`: The current content of the `textarea`.
   - Listens for `input` events on the `textarea` to detect changes.

2. **Server Code (Python)**:
   - Listens for WebSocket connections on port `6789`.
   - For each message received, it parses the JSON and extracts the `name` and `content` fields.
   - Prints the updated content of the `textarea` along with its ID.

### Running the Program

1. **Start the WebSocket Server**:
   Run the Python server with:
   ```bash
   python3 server.py
   ```

2. **Open the HTML Client**:
   Open `index.html` in a web browser. Ensure the browser has access to `ws://localhost:6789`.

Now, every time you type something in the `textarea`, the contents are sent to the server, where they are logged.
