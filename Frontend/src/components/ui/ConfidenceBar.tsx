import './ConfidenceBar.css';

export interface ConfidenceBarProps {
  /** The confidence percentage from 0 to 100 */
  value: number;
  /** Optional label to show next to the value defaults to 'CONFIDENCE'*/
  label?: string;
  /** Hide the text labels to just show the bar */
  hideText?: boolean;
}

export function ConfidenceBar({ value, label = 'CONFIDENCE', hideText = false }: ConfidenceBarProps) {
  // Ensure the value stays between 0 and 100
  const clampedValue = Math.min(Math.max(value, 0), 100);

  // Set base bar color 
  let barColorClass = 'confidence-bar-fill'; // Red 

  return (
    <div className="confidence-bar-wrapper w-full">
      {!hideText && (
        <div className="flex items-baseline justify-between mb-1">
          <span className="confidence-bar-label text-xs font-bold uppercase tracking-wider">
            {label}
          </span>
          <span className="confidence-bar-value text-sm font-bold">
            {clampedValue.toFixed(1)}%
          </span>
        </div>
      )}
      {/* Container */}
      <div className="confidence-bar-bg relative h-6 w-full overflow-hidden">
        {/* Animated Fill Bar */}
        <div 
          className={`confidence-bar-fill absolute inset-y-0 left-0 transition-all duration-700 ease-out ${barColorClass}`}
          style={{ width: `${clampedValue}%` }}
        />
        
        {/* Retro Grid Overlay */}
        <div className="confidence-bar-grid absolute inset-0 pointer-events-none" />
      </div>
    </div>
  );
}