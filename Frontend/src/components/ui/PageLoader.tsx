import React from 'react';

interface PageLoaderProps {
  message?: string;
}

export const PageLoader: React.FC<PageLoaderProps> = ({ message = 'Loading...' }) => {
  return (
    <div className="fixed inset-0 flex flex-col items-center justify-center bg-[#0a0a0a] z-50 animate-fadeIn">
      {/* Pit lane light sequence */}
      <div className="flex flex-col items-center gap-10">
        {/* F1 Start Lights */}
        <div className="flex flex-col items-center gap-3">
          {/* Light bar housing */}
          <div className="flex items-center gap-2 bg-[#111111] border border-[#1a1a1a] rounded-sm px-6 py-4 shadow-[0_0_40px_rgba(225,6,0,0.15)]">
            {[0, 1, 2, 3, 4].map((i) => (
              <div key={i} className="flex flex-col items-center gap-1.5">
                {/* Light pod */}
                <div
                  className="w-8 h-8 rounded-full border border-[#2a2a2a] bg-[#1a0000] animate-f1Light"
                  style={{
                    animationDelay: `${i * 0.3}s`,
                    boxShadow: `0 0 0px rgba(225, 6, 0, 0)`,
                  }}
                />
                {/* Stem */}
                <div className="w-1 h-3 bg-[#1a1a1a]" />
              </div>
            ))}
          </div>

          {/* Gantry bar */}
          <div className="w-64 h-1 bg-[#1a1a1a] rounded-full" />
        </div>

        {/* Racing stripe progress bar */}
        <div className="w-64 flex flex-col gap-2">
          <div className="relative w-full h-0.5 bg-[#1a1a1a] overflow-hidden">
            <div className="absolute inset-y-0 left-0 bg-[#e10600] animate-scanline" />
          </div>

          {/* Telemetry readout text */}
          <div className="flex justify-between items-center">
            <span className="text-[10px] text-[#333] tracking-[0.2em] uppercase font-mono">
              SYS
            </span>
            <span className="text-[10px] text-[#e10600] tracking-[0.2em] uppercase font-mono animate-pulse">
              ● LIVE
            </span>
          </div>
        </div>

        {/* Message */}
        <div className="flex flex-col items-center gap-1">
          <p className="text-[#555] text-xs tracking-[0.25em] uppercase font-mono">
            {message}
          </p>
          <div className="flex gap-1">
            {[0, 1, 2].map((i) => (
              <span
                key={i}
                className="w-1 h-1 rounded-full bg-[#333] animate-bounce"
                style={{ animationDelay: `${i * 0.2}s` }}
              />
            ))}
          </div>
        </div>
      </div>

      {/* Corner decoration — subtle track sector lines */}
      <div className="absolute bottom-8 left-8 right-8 flex justify-between items-end opacity-20">
        <div className="flex gap-1 items-end">
          <div className="w-8 h-0.5 bg-[#e10600]" />
          <div className="w-4 h-0.5 bg-[#555]" />
          <div className="w-2 h-0.5 bg-[#333]" />
        </div>
        <span className="text-[9px] text-[#333] tracking-widest font-mono uppercase">
          F1 Race Predictor
        </span>
        <div className="flex gap-1 items-end">
          <div className="w-2 h-0.5 bg-[#333]" />
          <div className="w-4 h-0.5 bg-[#555]" />
          <div className="w-8 h-0.5 bg-[#e10600]" />
        </div>
      </div>

      <style>{`
        @keyframes f1Light {
          0%, 40% { background-color: #1a0000; box-shadow: none; }
          50%, 90% { background-color: #e10600; box-shadow: 0 0 12px 4px rgba(225, 6, 0, 0.6), 0 0 30px 8px rgba(225, 6, 0, 0.2); }
          100% { background-color: #1a0000; box-shadow: none; }
        }
        @keyframes scanline {
          0% { left: -100%; width: 60%; }
          100% { left: 150%; width: 60%; }
        }
        @keyframes fadeIn {
          from { opacity: 0; }
          to { opacity: 1; }
        }
        .animate-f1Light {
          animation: f1Light 2.5s ease-in-out infinite;
        }
        .animate-scanline {
          animation: scanline 1.8s cubic-bezier(0.4, 0, 0.6, 1) infinite;
        }
        .animate-fadeIn {
          animation: fadeIn 0.4s ease-out forwards;
        }
      `}</style>
    </div>
  );
};
