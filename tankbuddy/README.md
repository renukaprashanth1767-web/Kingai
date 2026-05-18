# TankBuddy AI

Transform an old Android phone into a smart AI aquarium monitoring server using its camera, local storage, and lightweight AI models.

## Architecture & Tech Stack

**Frontend:** Next.js, React, Tailwind CSS, Framer Motion, Recharts
**Backend:** Node.js, Express, Socket.io
**AI Model:** TensorFlow.js (Running locally in-browser)
**Storage:** Local JSON Data Store

## Getting Started Locally (Development)

1. Clone the repository and navigate to the project root.
2. Install dependencies:
   ```bash
   cd tankbuddy/frontend && npm install
   cd ../backend && npm install
   ```
3. Start both servers:
   ```bash
   cd tankbuddy
   ./start.sh
   ```
4. Open your browser and navigate to `http://localhost:3000`.

## Android Old Phone Setup (Termux + Remote Access)

1. Install **Termux** from F-Droid (do not use Google Play version).
2. Open Termux and run the following commands to install dependencies:
   ```bash
   pkg update && pkg upgrade -y
   pkg install nodejs git -y
   ```
3. Clone your code onto the phone (or copy files over):
   ```bash
   git clone <your-repo-url>
   cd <repo-name>/tankbuddy
   ```
4. Install npm packages for both backend and frontend as you would normally.
5. Run `./start.sh` to begin the local node instance.
6. Open your phone's browser (e.g. Chrome) and navigate to `http://localhost:3000`.
7. Choose **Camera Server Node** and accept Camera permissions. Leave the phone screen on and plugged in.

### Remote Tunneling (Access from outside the house)

If you wish to view your dashboard from a completely remote location, run a tunnel app alongside Termux.

**Using Cloudflared:**
```bash
pkg install cloudflared
cloudflared tunnel --url http://localhost:3000
```
**Using Ngrok:**
```bash
pkg install wget
# Download ngrok ARM binary
wget https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-linux-arm.zip
unzip ngrok-stable-linux-arm.zip
./ngrok http 3000
```

Scan the provided tunnel URL or share it with your main phone.

## Security Warning
This MVP does not include authentication. Anyone with the tunnel URL can access the live stream. In the future, PIN login and secure web socket transmission will be implemented.
