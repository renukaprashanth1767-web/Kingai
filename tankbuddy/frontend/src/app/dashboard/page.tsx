"use client";

import { useEffect, useState } from "react";
import { io, Socket } from "socket.io-client";
import { motion } from "framer-motion";
import VideoPlayer from "@/components/VideoPlayer";
import Charts from "@/components/Charts";
import { Fish, Droplets, Thermometer, Utensils, AlertCircle } from "lucide-react";

export default function DashboardPage() {
  const [socket, setSocket] = useState<Socket | null>(null);
  const [currentScore, setCurrentScore] = useState(0);

  useEffect(() => {
    // In production, this would use window.location.hostname to find the backend
    const socketUrl = process.env.NEXT_PUBLIC_API_URL || "http://localhost:3001";
    const socketInstance = io(socketUrl);

    // Use timeout to prevent synchronous state update in effect body warning
    setTimeout(() => {
      setSocket(socketInstance);
    }, 0);

    socketInstance.on("activity-data", (data: { score: number }) => {
      setCurrentScore(data.score);
    });

    return () => {
      socketInstance.disconnect();
    };
  }, []);

  const handleFeed = async () => {
    try {
      const url = process.env.NEXT_PUBLIC_API_URL || "http://localhost:3001";
      await fetch(`${url}/api/feed`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ amount: "Normal" }),
      });
      alert("Feeding Logged!");
    } catch (error) {
      console.error("Failed to log feed", error);
    }
  };

  return (
    <div className="min-h-screen bg-black text-white p-4 md:p-8 font-sans selection:bg-emerald-500/30">
      <div className="max-w-6xl mx-auto space-y-6">

        {/* Header */}
        <header className="flex justify-between items-center mb-8">
          <div className="flex items-center gap-3">
             <div className="w-10 h-10 bg-gradient-to-br from-emerald-400 to-emerald-600 rounded-xl flex items-center justify-center shadow-lg shadow-emerald-500/20">
               <Fish className="text-white" size={24} />
             </div>
             <div>
               <h1 className="text-2xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-emerald-400 to-cyan-400">TankBuddy</h1>
               <p className="text-zinc-500 text-sm">Smart Monitoring Dashboard</p>
             </div>
          </div>
          <div className="flex gap-4">
             <button
               onClick={handleFeed}
               className="flex items-center gap-2 bg-zinc-900 hover:bg-zinc-800 transition-colors border border-zinc-800 px-4 py-2 rounded-xl text-emerald-400 font-medium shadow-xl">
                <Utensils size={18} /> Log Feeding
             </button>
          </div>
        </header>

        {/* Main Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">

           {/* Left Col - Video & Stats */}
           <div className="lg:col-span-2 space-y-6">
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                className="bg-zinc-900/40 p-2 rounded-2xl border border-zinc-800/50 backdrop-blur-xl"
              >
                <VideoPlayer socket={socket} />
              </motion.div>

              <motion.div
                 initial={{ opacity: 0, y: 20 }}
                 animate={{ opacity: 1, y: 0 }}
                 transition={{ delay: 0.1 }}
              >
                 <Charts socket={socket} />
              </motion.div>
           </div>

           {/* Right Col - Info Cards */}
           <div className="space-y-6">

              {/* Activity Card */}
              <motion.div
                initial={{ opacity: 0, x: 20 }}
                animate={{ opacity: 1, x: 0 }}
                className="bg-gradient-to-br from-zinc-900 to-zinc-950 p-6 rounded-2xl border border-zinc-800 relative overflow-hidden"
              >
                 <div className="absolute top-0 right-0 p-4 opacity-10">
                    <ActivityIcon size={120} />
                 </div>
                 <h3 className="text-zinc-400 font-medium mb-2 flex items-center gap-2">
                    <Fish size={18} /> Current Activity
                 </h3>
                 <div className="text-5xl font-bold text-emerald-400 mb-2">
                    {currentScore}<span className="text-2xl text-emerald-600">%</span>
                 </div>
                 <p className="text-sm text-zinc-500">
                    {currentScore > 50 ? "Fish are highly active right now." : "Fish are relatively calm."}
                 </p>
              </motion.div>

              {/* Status Cards */}
              <div className="grid grid-cols-2 gap-4">
                 <motion.div
                    initial={{ opacity: 0, scale: 0.9 }}
                    animate={{ opacity: 1, scale: 1 }}
                    transition={{ delay: 0.2 }}
                    className="bg-zinc-900/50 p-5 rounded-2xl border border-zinc-800/50 flex flex-col items-center text-center"
                 >
                    <Thermometer className="text-orange-400 mb-2" size={24} />
                    <span className="text-2xl font-bold">26°</span>
                    <span className="text-xs text-zinc-500">Water Temp</span>
                 </motion.div>

                 <motion.div
                    initial={{ opacity: 0, scale: 0.9 }}
                    animate={{ opacity: 1, scale: 1 }}
                    transition={{ delay: 0.3 }}
                    className="bg-zinc-900/50 p-5 rounded-2xl border border-zinc-800/50 flex flex-col items-center text-center"
                 >
                    <Droplets className="text-cyan-400 mb-2" size={24} />
                    <span className="text-2xl font-bold">Clear</span>
                    <span className="text-xs text-zinc-500">Water Quality</span>
                 </motion.div>
              </div>

              {/* System Alerts */}
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.4 }}
                className="bg-zinc-900/50 p-6 rounded-2xl border border-zinc-800/50"
              >
                 <h3 className="text-zinc-400 font-medium mb-4 flex items-center gap-2">
                    <AlertCircle size={18} /> System Alerts
                 </h3>
                 <div className="space-y-3">
                    <div className="flex items-center gap-3 text-sm p-3 bg-emerald-500/10 border border-emerald-500/20 rounded-xl text-emerald-300">
                       <div className="w-2 h-2 rounded-full bg-emerald-500" />
                       System operating normally. AI tracking active.
                    </div>
                 </div>
              </motion.div>

           </div>

        </div>
      </div>
    </div>
  );
}

// Simple internal icon
function ActivityIcon({ size }: { size: number }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <polyline points="22 12 18 12 15 21 9 3 6 12 2 12"></polyline>
    </svg>
  );
}
