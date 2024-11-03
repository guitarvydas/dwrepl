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
