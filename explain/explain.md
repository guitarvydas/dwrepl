Creating a WebSocket server and client in Python without using the `websockets` package requires handling the WebSocket handshake and managing frames manually, which can be tricky. Here’s a basic example that sets up a WebSocket server using `socket` and a WebSocket client, also using `socket`. This code is minimal and does not handle all the intricacies of the WebSocket protocol, but it will provide a simple, functioning WebSocket connection.

### Server Code (server.py)

The server will handle the WebSocket handshake and perform a basic echo of messages sent from the client.

```python
import socket
import base64
import hashlib

HOST = 'localhost'
PORT = 6789

# WebSocket handshake response
def create_handshake_response(websocket_key):
    magic_string = '258EAFA5-E914-47DA-95CA-C5AB0DC85B11'
    accept_key = base64.b64encode(hashlib.sha1((websocket_key + magic_string).encode()).digest()).decode()
    response = (
        "HTTP/1.1 101 Switching Protocols\r\n"
        "Upgrade: websocket\r\n"
        "Connection: Upgrade\r\n"
        f"Sec-WebSocket-Accept: {accept_key}\r\n\r\n"
    )
    return response

# Decoding WebSocket frame
def decode_frame(data):
    length = data[1] & 127
    if length == 126:
        mask = data[4:8]
        message = data[8:]
    elif length == 127:
        mask = data[10:14]
        message = data[14:]
    else:
        mask = data[2:6]
        message = data[6:]
    return bytes(b ^ mask[i % 4] for i, b in enumerate(message))

# Encoding WebSocket frame
def encode_frame(message):
    frame = [129]
    frame += [len(message)]
    frame_to_send = bytearray(frame) + message.encode()
    return frame_to_send

# Start WebSocket server
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(1)
print(f"WebSocket server running on ws://{HOST}:{PORT}")

client_socket, addr = server_socket.accept()
print(f"Connection from {addr}")

# Handle WebSocket handshake
request = client_socket.recv(1024).decode()
websocket_key = None
for line in request.splitlines():
    if line.startswith("Sec-WebSocket-Key: "):
        websocket_key = line.split(": ")[1]

handshake_response = create_handshake_response(websocket_key)
client_socket.send(handshake_response.encode())

# Echo messages
try:
    while True:
        data = client_socket.recv(1024)
        if not data:
            break
        message = decode_frame(data)
        print(f"Received: {message.decode()}")
        client_socket.send(encode_frame(f"Echo: {message.decode()}"))
except Exception as e:
    print(f"Error: {e}")
finally:
    client_socket.close()
    server_socket.close()
```

### Client Code (client.py)

The client connects to the WebSocket server, sends a message, and then receives an echo from the server.

```python
import socket
import base64
import hashlib

HOST = 'localhost'
PORT = 6789

# Decoding WebSocket frame
def decode_frame(data):
    length = data[1] & 127
    if length == 126:
        mask = data[4:8]
        message = data[8:]
    elif length == 127:
        mask = data[10:14]
        message = data[14:]
    else:
        mask = data[2:6]
        message = data[6:]
    return bytes(b ^ mask[i % 4] for i, b in enumerate(message))

# Encoding WebSocket frame
def encode_frame(message):
    frame = [129]
    frame += [len(message)]
    frame_to_send = bytearray(frame) + message.encode()
    return frame_to_send

# Connect to server and send WebSocket handshake
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

websocket_key = base64.b64encode(b"random_key").decode()
handshake_request = (
    "GET / HTTP/1.1\r\n"
    f"Host: {HOST}:{PORT}\r\n"
    "Upgrade: websocket\r\n"
    "Connection: Upgrade\r\n"
    f"Sec-WebSocket-Key: {websocket_key}\r\n"
    "Sec-WebSocket-Version: 13\r\n\r\n"
)
client_socket.send(handshake_request.encode())

# Receive the handshake response from the server
response = client_socket.recv(1024)
print("Handshake response received from server.")

# Send and receive messages
try:
    message = "Hello, WebSocket server!"
    client_socket.send(encode_frame(message))
    print(f"Sent: {message}")
    
    data = client_socket.recv(1024)
    decoded_message = decode_frame(data)
    print(f"Received: {decoded_message.decode()}")
finally:
    client_socket.close()
```

### Explanation of Key Parts

1. **Handshake**: The server completes the WebSocket handshake by computing a hash using `Sec-WebSocket-Key` and `Sec-WebSocket-Accept` headers, then sends it to the client.
2. **Encoding and Decoding Frames**: Both server and client handle the WebSocket frame format. Each message is masked (as per the WebSocket protocol) before sending, and unmasked upon receipt.
3. **Echo**: The server simply echoes the message back to the client as an acknowledgment.

This example demonstrates the basics but lacks the more advanced features, like handling larger frames, masking, closing frames, and error management. For production use, a library like `websockets` or a framework that supports WebSocket connections is generally more reliable and feature-complete.
