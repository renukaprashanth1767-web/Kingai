"use client";

import { useEffect, useState } from "react";
import { Socket } from "socket.io-client";
import { Video, WifiOff } from "lucide-react";

interface VideoPlayerProps {
  socket: Socket | null;
}

export default function VideoPlayer({ socket }: VideoPlayerProps) {
  const [frameSrc, setFrameSrc] = useState<string | null>(null);

  useEffect(() => {
    if (!socket) return;

    const handleVideoFrame = (data: string) => {
      setFrameSrc(data);
    };

    socket.on("video-frame", handleVideoFrame);

    return () => {
      socket.off("video-frame", handleVideoFrame);
    };
  }, [socket]);

  return (
    <div className="relative w-full aspect-video bg-zinc-900 rounded-xl overflow-hidden border border-zinc-800/50 shadow-2xl flex items-center justify-center">
      {frameSrc ? (
        <img
          src={frameSrc}
          alt="Live Aquarium Stream"
          className="w-full h-full object-cover"
        />
      ) : (
        <div className="flex flex-col items-center text-zinc-600 gap-3">
          <WifiOff size={48} className="opacity-50" />
          <p className="font-medium text-sm">Waiting for live stream...</p>
        </div>
      )}

      {/* Live Badge */}
      <div className="absolute top-4 right-4 flex items-center gap-2 bg-black/60 backdrop-blur-md px-3 py-1.5 rounded-full border border-red-500/30">
         <div className="w-2 h-2 rounded-full bg-red-500 animate-pulse" />
         <span className="text-xs font-bold text-red-500 tracking-wider">LIVE</span>
      </div>
    </div>
  );
}
