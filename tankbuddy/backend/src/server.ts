import express from 'express';
import http from 'http';
import { Server } from 'socket.io';
import cors from 'cors';
import { initDB, readDB, updateSetting, logActivity, logFeed } from './db';

const app = express();
const server = http.createServer(app);

// Allow any frontend origin for local MVP testing
const io = new Server(server, {
  cors: {
    origin: "*",
    methods: ["GET", "POST"]
  }
});

app.use(cors());
app.use(express.json());

// Initialize DB
initDB();

// API Routes
app.get('/api/data', (req, res) => {
  res.json(readDB());
});

app.post('/api/feed', (req, res) => {
  const { amount } = req.body;
  if (amount) {
    logFeed(amount);
    io.emit('new-feed', { timestamp: Date.now(), amount });
    res.json({ success: true });
  } else {
    res.status(400).json({ error: 'Amount is required' });
  }
});

// Socket.io for Realtime Communication
io.on('connection', (socket) => {
  console.log('Client connected:', socket.id);

  // Receive video frame from camera device, broadcast to remote viewers
  socket.on('video-frame', (data) => {
    // data should ideally be a base64 encoded jpeg
    socket.broadcast.emit('video-frame', data);
  });

  // Receive AI activity data from camera device
  socket.on('activity-data', (data: { score: number }) => {
    logActivity(data.score);
    // Broadcast real-time score to dashboard viewers
    socket.broadcast.emit('activity-data', data);
  });

  // Tunnel URL updates from startup scripts
  socket.on('update-tunnel', (data: { url: string }) => {
    updateSetting('tunnelUrl', data.url);
    socket.broadcast.emit('tunnel-updated', data.url);
  });

  socket.on('disconnect', () => {
    console.log('Client disconnected:', socket.id);
  });
});

const PORT = process.env.PORT || 3001;

server.listen(PORT, () => {
  console.log(`TankBuddy Backend running on port ${PORT}`);
});
