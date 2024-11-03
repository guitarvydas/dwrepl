import json
import asyncio
import websockets

async def handle_connection(websocket, path):
    async for message in websocket:
        data = json.loads(message)
        filename = data.get("filename", "")
        input_text = data.get("input", "")

        # Simulate processing
        output = f"Received filename: {filename} and input: {input_text}"
        probe_a = f"Probe A checked: {filename}"
        probe_b = f"Probe B analyzed: {input_text}"
        probe_c = f"Probe C diagnostic on: {filename}"
        errors = "" if filename and input_text else "Both filename and input are required"

        # Send back the updated output values
        response = {
            "output": output,
            "probeA": probe_a,
            "probeB": probe_b,
            "probeC": probe_c,
            "errors": errors
        }
        await websocket.send(json.dumps(response))

# Start WebSocket server
async def main():
    async with websockets.serve(handle_connection, "localhost", 6789):
        print("WebSocket server running on ws://localhost:6789")
        await asyncio.Future()  # Run forever

# Run the server
asyncio.run(main())
