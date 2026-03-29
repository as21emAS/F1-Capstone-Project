import './LoadingSkeleton.css';

export interface LoadingSkeletonProps {
  width?: string | number;
  height?: string | number;
  variant?: 'card' | 'table-row' | 'chart' | 'default';
  className?: string;
}

export function LoadingSkeleton({
  width,
  height,
  variant = 'default',
  className = '',
}: LoadingSkeletonProps) {
  return (
    <div
      className={`loading-skeleton skeleton-${variant} ${className}`}
      style={{ width, height }}
      aria-hidden="true"
    >
      {/* Optional internal scanline decoration for the retro vibe */}
      <div className="skeleton-scanlines absolute inset-0 pointer-events-none" />
    </div>
  );
}