HTML alone does not directly support WebSocket server (listener) capabilities because WebSockets are intended for client-server communication where the browser acts as the client. Browsers have no ability to act as a WebSocket server. However, you **can create a WebSocket client** in HTML/JavaScript to connect to a WebSocket server and listen for messages sent from that server.

Here’s how you can set up a **WebSocket client** in HTML and JavaScript to listen for incoming messages from a WebSocket server.

---

### Steps to Create a WebSocket Client Listener in HTML and JavaScript

1. **Set up an HTML file** with JavaScript to connect to a WebSocket server.
2. **Create a WebSocket connection** to a server and listen for messages.
3. **Display the incoming messages** on the page.

#### Example: HTML WebSocket Client

Here's an example HTML file with JavaScript to create a WebSocket client and listen for messages from the server.

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>WebSocket Client Listener</title>
</head>
<body>
    <h1>WebSocket Client</h1>
    
    <!-- Button to connect to the WebSocket server -->
    <button onclick="connectWebSocket()">Connect to WebSocket Server</button>
    
    <!-- Area to display incoming messages from the server -->
    <div id="messages"></div>

    <script>
        let socket;

        function connectWebSocket() {
            // Create a new WebSocket connection to the server
            socket = new WebSocket('ws://localhost:8080'); // Use your server URL here
            
            // Log when the connection opens
            socket.onopen = () => {
                console.log("Connected to the WebSocket server.");
                displayMessage("Connected to the WebSocket server.");
            };

            // Listen for messages from the WebSocket server
            socket.onmessage = (event) => {
                console.log("Message from server:", event.data);
                displayMessage("Server: " + event.data);
            };

            // Handle errors
            socket.onerror = (error) => {
                console.error("WebSocket error:", error);
            };

            // Handle connection closure
            socket.onclose = () => {
                console.log("Disconnected from WebSocket server.");
                displayMessage("Disconnected from WebSocket server.");
            };
        }

        // Function to display messages on the web page
        function displayMessage(message) {
            const messagesDiv = document.getElementById("messages");
            const messageElement = document.createElement("p");
            messageElement.textContent = message;
            messagesDiv.appendChild(messageElement);
        }
    </script>
</body>
</html>
```

### Explanation

- **WebSocket Initialization**: Clicking the "Connect to WebSocket Server" button triggers the `connectWebSocket` function, which establishes a WebSocket connection to the server.
- **Event Listeners**:
  - **`onopen`**: Triggered when the connection to the WebSocket server is successfully opened.
  - **`onmessage`**: Triggered whenever a message is received from the server. The message is displayed in the `#messages` div.
  - **`onerror`**: Triggered if an error occurs with the WebSocket connection.
  - **`onclose`**: Triggered when the WebSocket connection is closed, either by the client or server.

---

### Running and Testing the WebSocket Client

To test this WebSocket client, you need a WebSocket server running on the same host or accessible via a network (e.g., on `ws://localhost:8080` as specified). 

#### Example WebSocket Server in Node.js

To provide a WebSocket server for testing, here’s a simple Node.js server that will send a message to any connected client every few seconds:

1. **Install the WebSocket library** for Node.js:

   ```bash
   npm install ws
   ```

2. **Create the WebSocket Server** (e.g., `server.js`):

   ```javascript
   // server.js
   const WebSocket = require('ws');

   const wss = new WebSocket.Server({ port: 8080 });

   wss.on('connection', (ws) => {
       console.log("New client connected");

       // Send a message to the client every 5 seconds
       setInterval(() => {
           ws.send("Hello from the server!");
       }, 5000);

       // Log messages received from the client
       ws.on('message', (message) => {
           console.log("Received from client:", message);
       });

       // Handle client disconnect
       ws.on('close', () => {
           console.log("Client disconnected");
       });
   });

   console.log("WebSocket server running on ws://localhost:8080");
   ```

3. **Start the Server**:

   ```bash
   node server.js
   ```

When you open the `index.html` file in a browser and click the "Connect to WebSocket Server" button, it should connect to the WebSocket server and display incoming messages every 5 seconds.

---

### Summary

- **HTML and JavaScript** only allow you to create a WebSocket client, not a server.
- The JavaScript WebSocket client listens for messages from a server and displays them on the page.
- A WebSocket server, like the Node.js example provided, sends messages to connected clients, allowing real-time updates to be pushed to the client.

This setup is ideal for applications requiring real-time data updates, such as live notifications, chat applications, and collaborative tools.
