#!/bin/bash

# Ensure we're in the right directory
cd "$(dirname "$0")"

echo "==========================================="
echo "🐟 Starting TankBuddy AI Platform 🐟"
echo "==========================================="

echo "1. Starting Backend API and Socket.io server..."
cd backend
npm run dev > ../backend.log 2>&1 &
BACKEND_PID=$!
echo "Backend running on port 3001 (PID: $BACKEND_PID)"

echo "2. Starting Frontend Next.js app..."
cd ../frontend
npm run dev > ../frontend.log 2>&1 &
FRONTEND_PID=$!
echo "Frontend running on port 3000 (PID: $FRONTEND_PID)"

echo ""
echo "==========================================="
echo "✅ Local Environment is UP"
echo "Open your browser to http://localhost:3000"
echo "==========================================="
echo ""
echo "To access remotely using an old Android phone via Termux:"
echo "1. Connect your phone to this network"
echo "2. Find your local IP address (e.g. 192.168.1.X)"
echo "3. Open http://<YOUR_IP>:3000 on the phone"
echo ""
echo "Or use a tunnel for public internet access:"
echo "cloudflared: 'cloudflared tunnel --url http://localhost:3000'"
echo "ngrok:       'ngrok http 3000'"
echo ""
echo "Press Ctrl+C to stop all services"

# Wait for Ctrl+C
trap "echo 'Stopping TankBuddy...'; kill $BACKEND_PID; kill $FRONTEND_PID; exit 0" SIGINT SIGTERM

wait
