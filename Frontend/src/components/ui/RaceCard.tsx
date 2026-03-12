import './RaceCard.css';

export interface RaceCardProps {
  race_id: string;
  name: string;
  circuit: string;
  date: string;
  round: number;
  season: number;
}

export function RaceCard({
  race_id,
  name,
  circuit,
  date,
  round,
  season,
}: RaceCardProps) {
  return (
    <div className="race-card relative overflow-hidden">
      {/* Grid Pattern Background */}
      <div className="race-card-grid-pattern absolute inset-0 opacity-5" />
      
      {/* Optional CRT Scanlines Effect */}
      <div className="race-card-scanlines absolute inset-0 pointer-events-none" />

      {/* Top Color Bar */}
      <div className="race-card-top-bar flex h-1.5">
        <div className="race-card-top-bar-red" />
        <div className="race-card-top-bar-black" />
      </div>

      {/* Content */}
      <div className="race-card-content relative p-3">
        {/* Header with Round */}
        <div className="mb-3">
          {/* Round Label */}
          <div className="flex items-baseline gap-2 mb-0.5">
            <span className="race-card-label text-xs font-bold uppercase tracking-widest">
              ROUND
            </span>
          </div>
          {/* Round Number with 3D effect */}
          <div className="race-card-round text-4xl font-bold leading-none mb-2">
            {round.toString().padStart(2, '0')}
          </div>
          
          {/* Divider Line with 3D inset */}
          <div className="race-card-divider mb-2" />
          
          {/* Race Name */}
          <h3 className="race-card-header text-lg font-bold uppercase tracking-wide mb-0">
            {name}
          </h3>
        </div>

        {/* Info Section - Circuit and Date */}
        <div className="space-y-2">
          {/* Circuit */}
          <div className="flex items-baseline gap-2">
            <span className="race-card-label text-xs font-bold uppercase tracking-wider">
              CIRCUIT
            </span>
            <span className="race-card-info text-sm font-medium">
              {circuit}
            </span>
          </div>
          
          {/* Date */}
          <div className="flex items-baseline gap-2">
            <span className="race-card-label text-xs font-bold uppercase tracking-wider">
              DATE
            </span>
            <span className="race-card-info text-sm font-medium">
              {date}
            </span>
          </div>
           {/* Season */}
          <div className="flex items-baseline gap-2">
            <span className="race-card-label text-xs font-bold uppercase tracking-wider">
              SEASON
            </span>
            <span className="race-card-info text-sm font-medium">
              {season}
            </span>
          </div>
        </div>
      </div>

      {/* Side Accent Stripes with 3D effect */}
      <div className="race-card-side-stripe absolute top-0 right-0 w-2 h-full flex flex-col">
        <div className="race-card-side-stripe-segment race-card-side-stripe-red flex-1" />
        <div className="race-card-side-stripe-segment race-card-side-stripe-black flex-1" />
      </div>
    </div>
  );
}
