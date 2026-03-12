import React from 'react';

interface EmptyStateProps {
  icon?: React.ReactNode;
  title: string;
  message: string;
  actionLabel?: string;
  onAction?: () => void;
}

// Default F1 flag icon
const DefaultFlagIcon: React.FC = () => (
  <svg
    viewBox="0 0 40 40"
    fill="none"
    className="w-10 h-10"
    aria-hidden="true"
  >
    {/* Flag pole */}
    <line x1="8" y1="4" x2="8" y2="36" stroke="#333" strokeWidth="1.5" strokeLinecap="round" />
    {/* Checkered flag - 4x3 grid */}
    {[0, 1, 2, 3].map((col) =>
      [0, 1, 2].map((row) => (
        <rect
          key={`${col}-${row}`}
          x={8 + col * 6}
          y={4 + row * 6}
          width={6}
          height={6}
          fill={(col + row) % 2 === 0 ? '#2a2a2a' : '#1a1a1a'}
        />
      ))
    )}
    {/* Flag outline */}
    <rect x="8" y="4" width="24" height="18" stroke="#2a2a2a" strokeWidth="0.75" fill="none" />
  </svg>
);

export const EmptyState: React.FC<EmptyStateProps> = ({
  icon,
  title,
  message,
  actionLabel,
  onAction,
}) => {
  return (
    <div className="flex flex-col items-center justify-center py-12 px-6 text-center">
      {/* Icon area */}
      <div className="mb-4 opacity-60">
        {icon ?? <DefaultFlagIcon />}
      </div>

      {/* Thin divider */}
      <div className="flex items-center gap-2 mb-5 w-24">
        <div className="flex-1 h-px bg-[#1e1e1e]" />
        <div className="w-1 h-1 bg-[#2a2a2a] rotate-45" />
        <div className="flex-1 h-px bg-[#1e1e1e]" />
      </div>

      {/* Text */}
      <p className="text-[#555] text-xs tracking-[0.2em] uppercase font-mono mb-1.5">
        {title}
      </p>
      <p className="text-[#383838] text-xs font-mono max-w-xs leading-relaxed">
        {message}
      </p>

      {/* Optional action */}
      {actionLabel && onAction && (
        <button
          onClick={onAction}
          className="mt-5 px-4 py-2 border border-[#2a2a2a] hover:border-[#e10600]/40 text-[#444] hover:text-[#888] text-[11px] font-mono tracking-[0.15em] uppercase transition-colors duration-150 focus:outline-none focus:ring-1 focus:ring-[#e10600]/30"
        >
          {actionLabel}
        </button>
      )}
    </div>
  );
};
