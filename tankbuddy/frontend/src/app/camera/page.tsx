"use client";

import { useEffect, useRef, useState } from "react";
import { io, Socket } from "socket.io-client";
import { processFrame } from "@/lib/ai-engine";
import { Camera, Activity, Server, ShieldCheck } from "lucide-react";

export default function CameraPage() {
  const videoRef = useRef<HTMLVideoElement>(null);
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const [socket, setSocket] = useState<Socket | null>(null);
  const [isConnected, setIsConnected] = useState(false);
  const [activityScore, setActivityScore] = useState(0);

  useEffect(() => {
    // Connect to local backend (assumes backend runs on same device, port 3001)
    const socketInstance = io("http://localhost:3001");
    // Use timeout to prevent synchronous state update in effect body warning
    setTimeout(() => {
      setSocket(socketInstance);
    }, 0);

    socketInstance.on("connect", () => setIsConnected(true));
    socketInstance.on("disconnect", () => setIsConnected(false));

    return () => {
      socketInstance.disconnect();
    };
  }, []);

  useEffect(() => {
    let animationFrameId: number;
    let stream: MediaStream | null = null;

    const startCamera = async () => {
      try {
        stream = await navigator.mediaDevices.getUserMedia({
          video: { facingMode: "environment", width: 640, height: 480 },
          audio: false,
        });

        if (videoRef.current) {
          videoRef.current.srcObject = stream;
          videoRef.current.play();
        }
      } catch (err) {
        console.error("Error accessing camera:", err);
      }
    };

    startCamera();

    const captureAndProcessFrame = async () => {
      if (videoRef.current && canvasRef.current && socket) {
        const video = videoRef.current;
        const canvas = canvasRef.current;
        const ctx = canvas.getContext("2d", { willReadFrequently: true });

        if (ctx && video.readyState === video.HAVE_ENOUGH_DATA) {
          canvas.width = video.videoWidth;
          canvas.height = video.videoHeight;
          ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

          // Stream JPEG frame to backend
          const frameData = canvas.toDataURL("image/jpeg", 0.5); // compress quality
          socket.emit("video-frame", frameData);

          // Process AI Activity Score
          const score = await processFrame(video);
          if (score !== null) {
             setActivityScore(Math.round(score * 100));
             socket.emit("activity-data", { score: Math.round(score * 100) });
          }
        }
      }

      // limit frame processing/streaming to ~10 FPS to save old phone battery
      setTimeout(() => {
         animationFrameId = requestAnimationFrame(captureAndProcessFrame);
      }, 100);
    };

    videoRef.current?.addEventListener('loadeddata', () => {
      captureAndProcessFrame();
    });

    return () => {
      if (animationFrameId) cancelAnimationFrame(animationFrameId);
      if (stream) stream.getTracks().forEach((track) => track.stop());
    };
  }, [socket]);

  return (
    <div className="min-h-screen bg-black text-emerald-400 p-6 flex flex-col items-center">
      <div className="max-w-md w-full flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold flex items-center gap-2">
          <Camera className="text-emerald-500" /> TankBuddy Node
        </h1>
        <div className={`px-3 py-1 rounded-full text-xs font-bold ${isConnected ? 'bg-emerald-900 text-emerald-300' : 'bg-red-900 text-red-300'}`}>
          {isConnected ? "Connected" : "Disconnected"}
        </div>
      </div>

      <div className="relative w-full max-w-md rounded-2xl overflow-hidden border border-zinc-800 shadow-2xl shadow-emerald-900/20">
        <video
          ref={videoRef}
          className="w-full h-auto object-cover bg-zinc-900"
          playsInline
          muted
        />
        <canvas ref={canvasRef} className="hidden" />

        {/* Overlay HUD */}
        <div className="absolute top-4 left-4 bg-black/60 backdrop-blur-md rounded-lg p-2 text-xs flex flex-col gap-1 border border-zinc-700/50">
           <div className="flex items-center gap-2">
              <Activity size={14} className="text-emerald-400" />
              <span>AI Activity: {activityScore}%</span>
           </div>
           <div className="flex items-center gap-2">
              <Server size={14} className="text-blue-400" />
              <span>Streaming Mode</span>
           </div>
        </div>
      </div>

      <div className="mt-8 max-w-md w-full bg-zinc-900/50 p-6 rounded-2xl border border-zinc-800">
         <h2 className="text-sm text-zinc-400 mb-4 flex items-center gap-2 uppercase tracking-wider">
           <ShieldCheck size={16} /> Device Status
         </h2>
         <div className="space-y-3 text-sm">
            <div className="flex justify-between">
              <span className="text-zinc-500">Camera</span>
              <span className="text-emerald-400">Active</span>
            </div>
            <div className="flex justify-between">
              <span className="text-zinc-500">AI Engine</span>
              <span className="text-emerald-400">Local TF.js</span>
            </div>
            <div className="flex justify-between">
              <span className="text-zinc-500">Local DB</span>
              <span className="text-emerald-400">Writing Logs</span>
            </div>
         </div>
      </div>
    </div>
  );
}
