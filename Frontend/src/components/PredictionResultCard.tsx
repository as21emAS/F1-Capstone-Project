import './PredictionResultCard.css';
import { ConfidenceBar } from './index';

export interface PredictionResultCardProps {
  driver: string;
  predicted_position: number;
  confidence_score: number; // 0-100
}

export function PredictionResultCard({
  driver,
  predicted_position,
  confidence_score,
}: PredictionResultCardProps) {
  return (
    <div className="prediction-card relative overflow-hidden">
      {/* Grid Pattern Background */}
      <div className="prediction-card-grid-pattern absolute inset-0 opacity-5" />
      
      {/* Optional CRT Scanlines Effect */}
      <div className="prediction-card-scanlines absolute inset-0 pointer-events-none" />

      {/* Top Color Bar */}
      <div className="prediction-card-top-bar h-1.5" />

      {/* Content */}
      <div className="prediction-card-content relative p-3">
        {/* Header with Predicted Position */}
        <div className="mb-3">
          {/* Position Label */}
          <div className="flex items-baseline gap-2 mb-0.5">
            <span className="prediction-card-label text-xs font-bold uppercase tracking-widest">
              PREDICTED P
            </span>
          </div>
          {/* Position Number with 3D effect */}
          <div className="prediction-card-position text-4xl font-bold leading-none mb-2">
            {predicted_position.toString().padStart(2, '0')}
          </div>
          
          {/* Divider Line with 3D inset */}
          <div className="prediction-card-divider mb-2" />
          
          {/* Driver Name */}
          <h3 className="prediction-card-header text-lg font-bold uppercase tracking-wide mb-0">
            {driver}
          </h3>
        </div>

        {/* Confidence Section */}
        <div className="mt-4">
          <ConfidenceBar value={confidence_score} />
          </div>
        </div>

      {/* Side Accent Stripes with 3D effect */}
      <div className="prediction-card-side-stripe absolute top-0 right-0 w-2 h-full" />
    </div>
  );
}