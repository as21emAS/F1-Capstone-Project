import { getTeamColor } from './DriverCard';
import './TeamCard.css';

export interface TeamCardProps {
  team_id: string;
  name: string;
  points: number;
  position: number;
  wins: number;
  teamColor?: string;
  showScanlines?: boolean;
}

export function TeamCard({
  name,
  points,
  position,
  wins,
  teamColor,
  showScanlines = true,
}: TeamCardProps) {
  const color = teamColor || getTeamColor(name);
  
  return (
    <div className="team-card relative overflow-hidden">
      {/* Grid Pattern Background */}
      <div className="team-card-grid-pattern absolute inset-0 pointer-events-none opacity-[0.03]" />

      {/* Scanlines */}
      {showScanlines && (
        <div className="team-card-scanlines absolute inset-0 pointer-events-none" />
      )}

      {/* Top Bar - Team Color Accent */}
      <div className="team-card-top-bar flex h-3 relative">
        <div className="team-card-top-bar-red" />
        <div className="team-card-top-bar-team" style={{ background: color }} />
        <div className="team-card-top-bar-black" />
      </div>

      {/* Content */}
      <div className="team-card-content relative p-3">
        {/* Header with Position */}
        <div className="mb-3">
          {/* Position Label */}
          <div className="flex items-baseline gap-2 mb-0.5">
            <span className="team-card-label text-xs font-bold uppercase tracking-widest">
              POSITION
            </span>
          </div>
          {/* Position Number */}
          <div className="team-card-position text-4xl font-bold leading-none mb-2">
            {position.toString().padStart(2, '0')}
          </div>
          {/* Divider Line */}
          <div className="team-card-divider mb-2" />
           {/* Team Name */}
          <h3 className="team-card-header text-lg font-bold uppercase tracking-wide mb-0">
            {name}
          </h3>
        </div>
        {/* Stats Row */}
        <div className="flex items-center gap-4">
          <div className="team-card-stat">
            <strong className="text-xl font-bold">{points}</strong>
            <span className="team-card-stat-label text-xs uppercase tracking-wider ml-1">PTS</span>
          </div>
          <div className="team-card-divider-vertical w-px h-6" />
          <div className="team-card-stat">
            <strong className="text-xl font-bold">{wins}</strong>
            <span className="team-card-stat-label text-xs uppercase tracking-wider ml-1">WINS</span>
          </div>
        </div>
      </div>

      {/* Side Accent Stripes */}
      <div className="team-card-side-stripe absolute left-0 top-1/2 -translate-y-1/2 w-1 h-16 flex flex-col gap-1">
        <div className="team-card-side-stripe-segment flex-1" style={{ background: color }} />
        <div className="team-card-side-stripe-red flex-1" />
        <div className="team-card-side-stripe-black flex-1" />
      </div>
    </div>
  );
}