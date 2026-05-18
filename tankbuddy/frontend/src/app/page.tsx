import Link from "next/link";
import { Camera, LayoutDashboard, Fish } from "lucide-react";

export default function LandingPage() {
  return (
    <div className="min-h-screen bg-black flex flex-col items-center justify-center p-6 text-zinc-300 font-sans">

      <div className="text-center mb-12">
        <div className="w-20 h-20 bg-gradient-to-br from-emerald-400 to-cyan-500 rounded-2xl flex items-center justify-center mx-auto mb-6 shadow-2xl shadow-emerald-500/20">
          <Fish className="text-white w-10 h-10" />
        </div>
        <h1 className="text-4xl md:text-5xl font-extrabold text-white tracking-tight mb-4">
          TankBuddy AI
        </h1>
        <p className="text-zinc-500 text-lg max-w-md mx-auto">
          Transform your old Android phone into a smart aquarium monitor. Choose an operating mode below.
        </p>
      </div>

      <div className="grid md:grid-cols-2 gap-6 w-full max-w-4xl">

        {/* Camera Node Mode */}
        <Link href="/camera" className="group">
          <div className="bg-zinc-900/50 hover:bg-zinc-800/80 border border-zinc-800 hover:border-emerald-500/50 transition-all duration-300 rounded-3xl p-8 h-full flex flex-col items-center text-center cursor-pointer shadow-xl">
            <div className="w-16 h-16 rounded-full bg-emerald-500/10 text-emerald-400 flex items-center justify-center mb-6 group-hover:scale-110 transition-transform">
              <Camera size={32} />
            </div>
            <h2 className="text-2xl font-bold text-white mb-3">Camera Server Node</h2>
            <p className="text-zinc-500 text-sm leading-relaxed mb-6">
              Launch this on your old phone placed near the aquarium. It will activate the camera, process AI locally, and host the data stream.
            </p>
            <div className="mt-auto text-emerald-500 font-medium text-sm flex items-center gap-2 group-hover:gap-3 transition-all">
              Start Node &rarr;
            </div>
          </div>
        </Link>

        {/* Remote Dashboard Mode */}
        <Link href="/dashboard" className="group">
          <div className="bg-zinc-900/50 hover:bg-zinc-800/80 border border-zinc-800 hover:border-cyan-500/50 transition-all duration-300 rounded-3xl p-8 h-full flex flex-col items-center text-center cursor-pointer shadow-xl">
            <div className="w-16 h-16 rounded-full bg-cyan-500/10 text-cyan-400 flex items-center justify-center mb-6 group-hover:scale-110 transition-transform">
              <LayoutDashboard size={32} />
            </div>
            <h2 className="text-2xl font-bold text-white mb-3">Remote Dashboard</h2>
            <p className="text-zinc-500 text-sm leading-relaxed mb-6">
              Launch this on your personal phone or computer to view live streams, AI analytics, and control the system remotely.
            </p>
            <div className="mt-auto text-cyan-500 font-medium text-sm flex items-center gap-2 group-hover:gap-3 transition-all">
              Open Dashboard &rarr;
            </div>
          </div>
        </Link>

      </div>

    </div>
  );
}
