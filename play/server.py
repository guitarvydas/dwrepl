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
