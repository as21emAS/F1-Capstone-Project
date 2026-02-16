export default function Dashboard() {
  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold border-l-4 border-red-600 pl-4">Race Dashboard</h1>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="bg-gray-800 p-6 rounded-lg shadow-lg">
          <h2 className="text-xl font-semibold mb-4">Next Race Prediction</h2>
          <p className="text-gray-400">Real-time ML prediction goes here...</p>
        </div>
        <div className="bg-gray-800 p-6 rounded-lg shadow-lg">
          <h2 className="text-xl font-semibold mb-4">Driver Standings</h2>
          <p className="text-gray-400">Current season ranking leaderboard...</p>
        </div>
      </div>
    </div>
  );
}
