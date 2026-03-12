import './DriverCard.css';

export interface DriverCardProps {
  driver_id: string;
  name: string;
  team: string;
  nationality: string;
  points: number;
  position: number;
  teamColor?: string;
  showScanlines?: boolean;
}

export const getTeamColor = (teamName: string): string => {
  const name = teamName.toLowerCase();
  
  if (name.includes('red bull')) return '#0600ef';      // Red Bull Blue
  if (name.includes('ferrari')) return '#ef1a2d';       // Ferrari Red
  if (name.includes('mclaren')) return '#ff8000';       // McLaren Papaya
  if (name.includes('mercedes')) return '#00a19c';      // Mercedes Teal
  if (name.includes('aston martin')) return '#00665e';  // Aston Green
  if (name.includes('alpine')) return '#0090ff';        // Alpine Blue
  if (name.includes('williams')) return '#005aff';      // Williams Blue
  if (name.includes('sauber') || name.includes('stake')) return '#00e701'; // Kick Sauber Green
  if (name.includes('haas')) return '#ffffff';          // Haas White
  if (name.includes('rb') || name.includes('alphatauri')) return '#6692ff'; // VCARB Blue
  
  return '#C41E3A'; // Fallback color if team is not found
};

export function DriverCard({
  name,
  team,
  nationality,
  points,
  position,
  teamColor,
  showScanlines = true,
}: DriverCardProps) {
  const color = teamColor || getTeamColor(team);
  
  return (
    <div className="driver-card relative overflow-hidden">
      {/* Grid Pattern Background */}
      <div className="driver-card-grid-pattern absolute inset-0 pointer-events-none opacity-[0.03]" />

      {/* Scanlines */}
      {showScanlines && (
        <div className="driver-card-scanlines absolute inset-0 pointer-events-none" />
      )}

      {/* Top Bar - Team Color Accent */}
      <div className="driver-card-top-bar flex h-3 relative">
        <div className="driver-card-top-bar-red" />
        <div className="driver-card-top-bar-team" style={{ background: color }} />
        <div className="driver-card-top-bar-black" />
      </div>

      {/* Content */}
      <div className="driver-card-content relative p-3">
        {/* Header Section */}
        <div className="flex items-start justify-between mb-2">
          <div>
            {/* Position Label */}
            <div className="flex items-baseline gap-2 mb-0.5">
              <span className="driver-card-label text-xs font-bold uppercase tracking-widest">
                POSITION
              </span>
            </div>
            {/* Position Number */}
            <div className="driver-card-position text-4xl font-bold leading-none">
              {position.toString().padStart(2, '0')}
            </div>
          </div>
        </div>

        {/* Divider Line */}
        <div className="driver-card-divider mb-2" />

        {/* Driver Name */}
        <div className="driver-card-name text-xl font-bold mb-1 uppercase tracking-wide leading-tight">
          {name}
        </div>

        {/* Nationality */}
        <div className="driver-card-nationality text-xs mb-3 uppercase font-bold">
          {nationality}
        </div>

        {/* Points Section */}
        <div className="mb-3">
          <div className="driver-card-label text-xs mb-1.5 uppercase tracking-widest font-bold">
            CHAMPIONSHIP PTS
          </div>
          
          {/* Points Display */}
          <div className="driver-card-points-box inline-block px-4 py-2 border-2 border-black">
            <div className="driver-card-points-value text-3xl font-bold leading-none">
              {points}
            </div>
          </div>
        </div>

        {/* Team Section */}
        <div>
          <div className="driver-card-label text-xs mb-1.5 uppercase tracking-widest font-bold">
            TEAM
          </div>
          <div className="driver-card-team-box border-2 border-black p-2 flex items-center justify-between">
            <div className="driver-card-team-name text-xs font-bold uppercase tracking-wider flex-1">
              {team}
            </div>
            <div className="flex gap-1">
              <div className="driver-card-team-stripe w-1.5 h-4" style={{ background: color }} />
              <div className="driver-card-team-stripe-red w-1.5 h-4" />
            </div>
          </div>
        </div>
      </div>
      {/* Side Accent Stripes */}
      <div className="driver-card-side-stripe absolute left-0 top-1/2 -translate-y-1/2 w-1 h-16 flex flex-col gap-1">
        <div className="driver-card-side-stripe-segment flex-1" style={{ background: color }} />
        <div className="driver-card-side-stripe-red flex-1" />
        <div className="driver-card-side-stripe-black flex-1" />
      </div>
    </div>
  );
}