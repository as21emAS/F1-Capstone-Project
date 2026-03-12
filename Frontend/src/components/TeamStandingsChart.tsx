import {
  PieChart,
  Pie,
  Cell,
  ResponsiveContainer,
  Tooltip,
  Legend,
} from 'recharts';
import './TeamStandingsChart.css';

export interface TeamStanding {
  position: number;
  name: string;
  points: number;
  wins?: number;
  team_id?: string;
  teamColor?: string;
}

export interface TeamStandingsChartProps {
  standings: TeamStanding[];
}

// Team colors for visual variety
const teamColors: Record<string, string> = {
  'Oracle Red Bull Racing': '#1E3A8A',
  'Mercedes-AMG Petronas': '#00D2BE',
  'Scuderia Ferrari': '#DC0000',
  'McLaren F1 Team': '#FF8700',
  'Aston Martin Aramco': '#006F62',
  'Red Bull Racing': '#0600EF',
  'Ferrari': '#DC0000',
  'Mercedes': '#00D2BE',
  'McLaren': '#FF8700',
  'Aston Martin': '#006F62',
  'Alpine': '#0090FF',
  'Williams': '#005AFF',
  'AlphaTauri': '#2B4562',
  'Alfa Romeo': '#900000',
  'Haas': '#FFFFFF',
};

export function TeamStandingsChart({ standings }: TeamStandingsChartProps) {
  // Transform data for pie chart
  const chartData = standings.map((team) => ({
    name: team.name,
    value: team.points,
    position: team.position,
    wins: team.wins,
    color: team.teamColor || teamColors[team.name] || '#C41E3A',
  }));

  // Custom tooltip
  const CustomTooltip = ({ active, payload }: any) => {
    if (active && payload && payload.length) {
      const data = payload[0].payload;
      return (
        <div className="team-chart-tooltip">
          <p className="team-chart-tooltip-name">{data.name}</p>
          <p className="team-chart-tooltip-position">P{data.position}</p>
          <p className="team-chart-tooltip-points">{data.value} PTS</p>
          <p className="team-chart-tooltip-wins">{data.wins} WINS</p>
        </div>
      );
    }
    return null;
  };

  // Custom legend
  const CustomLegend = ({ payload }: any) => {
    return (
      <div className="team-chart-legend">
        {payload.map((entry: any, index: number) => (
          <div key={`legend-${index}`} className="team-chart-legend-item">
            <div
              className="team-chart-legend-color"
              style={{ backgroundColor: entry.color }}
            />
            <span className="team-chart-legend-text">{entry.value}</span>
          </div>
        ))}
      </div>
    );
  };

  return (
    <div className="team-chart-container">
      {/* Chart Header */}
      <div className="team-chart-header">
        <div className="team-chart-top-bar" />
        <div className="team-chart-title-section">
          <h3 className="team-chart-title">TEAM STANDINGS</h3>
          <div className="team-chart-subtitle">POINTS</div>
        </div>
      </div>

      {/* Chart */}
      <div className="team-chart-wrapper">
        <ResponsiveContainer width="100%" height={260}>
          <PieChart margin={{ top: 10, right: 10, left: 10, bottom: 10 }}>
            <Pie
              data={chartData}
              cx="50%"
              cy="45%"
              labelLine={false}
              label={({ cx, cy, midAngle, innerRadius, outerRadius, percent }) => {
                const RADIAN = Math.PI / 180;
                const radius = outerRadius + 18;
                const x = cx + radius * Math.cos(-midAngle * RADIAN);
                const y = cy + radius * Math.sin(-midAngle * RADIAN);
                return (
                  <text
                    x={x}
                    y={y}
                    fill="#000"
                    textAnchor={x > cx ? 'start' : 'end'}
                    dominantBaseline="central"
                    style={{ 
                      fontSize: '13px', 
                      fontWeight: 'bold',
                      fontFamily: 'monospace'
                    }}
                  >
                    {`${(percent * 100).toFixed(0)}%`}
                  </text>
                );
              }}
              outerRadius={65}
              innerRadius={28}
              fill="#8884d8"
              dataKey="value"
              stroke="#000"
              strokeWidth={2}
            >
              {chartData.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={entry.color} />
              ))}
            </Pie>
            <Tooltip content={<CustomTooltip />} />
            <Legend content={<CustomLegend />} />
          </PieChart>
        </ResponsiveContainer>
      </div>

      {/* Side Stripe */}
      <div className="team-chart-side-stripe" />
    </div>
  );
}