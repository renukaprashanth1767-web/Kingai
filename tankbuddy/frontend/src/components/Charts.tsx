"use client";

import { useEffect, useState } from "react";
import { Socket } from "socket.io-client";
import { AreaChart, Area, XAxis, YAxis, Tooltip, ResponsiveContainer } from "recharts";

interface ChartsProps {
  socket: Socket | null;
}

export default function Charts({ socket }: ChartsProps) {
  const [data, setData] = useState<{ time: string; score: number }[]>([]);

  useEffect(() => {
    // initial fetch could happen here, for MVP we just build real-time array
    if (!socket) return;

    const handleActivity = (payload: { score: number }) => {
      setData((prev) => {
        const now = new Date();
        const timeStr = `${now.getHours()}:${now.getMinutes().toString().padStart(2, '0')}:${now.getSeconds().toString().padStart(2, '0')}`;

        const newRecord = { time: timeStr, score: payload.score };
        const newData = [...prev, newRecord];

        // keep last 20 data points
        if (newData.length > 20) {
          return newData.slice(newData.length - 20);
        }
        return newData;
      });
    };

    socket.on("activity-data", handleActivity);

    return () => {
      socket.off("activity-data", handleActivity);
    };
  }, [socket]);

  return (
    <div className="w-full h-64 bg-zinc-900/50 rounded-xl border border-zinc-800/50 p-4">
      <h3 className="text-sm font-medium text-zinc-400 mb-4">Live Activity Trend</h3>
      <div className="w-full h-48">
        <ResponsiveContainer width="100%" height="100%">
          <AreaChart data={data}>
            <defs>
              <linearGradient id="colorScore" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#10b981" stopOpacity={0.3} />
                <stop offset="95%" stopColor="#10b981" stopOpacity={0} />
              </linearGradient>
            </defs>
            <XAxis dataKey="time" hide />
            <YAxis hide domain={[0, 100]} />
            <Tooltip
              contentStyle={{ backgroundColor: '#18181b', border: '1px solid #27272a', borderRadius: '8px' }}
              itemStyle={{ color: '#10b981' }}
            />
            <Area
              type="monotone"
              dataKey="score"
              stroke="#10b981"
              fillOpacity={1}
              fill="url(#colorScore)"
              strokeWidth={2}
              isAnimationActive={false}
            />
          </AreaChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
