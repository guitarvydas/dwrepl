const express = require('express');
const http = require('http');
const { Server } = require('socket.io');
const path = require('path');

const app = express();
const server = http.createServer(app);
const io = new Server(server);

// Serve index.html explicitly when a user accesses the root URL
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'console.html'));
});

// Serve other static files (e.g., for Socket.IO)
app.use('/socket.io', express.static(path.join(__dirname, 'node_modules/socket.io/client-dist')));

// Handle WebSocket connections
io.on('connection', (socket) => {
    console.log('user connected');

    socket.on('input_changed', (data) => {
        const { filename, input } = data;

        // Simulated processing logic
        const output = `Received filename: ${filename} and input: ${input}`;
        const probeA = `Probe A: ${filename}`;
        const probeB = `Probe B: ${input}`;
        const probeC = `Probe C: ${filename}`;
        const errors = filename && input ? "" : "Both filename and input are required";

        // Send back updated output values
        socket.emit('update_outputs', { output, probeA, probeB, probeC, errors });
    });

    socket.on('disconnect', () => {
        console.log('user disconnected');
    });
});

// Start the server
const PORT = 3000;
server.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});
