import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'

import { BrowserRouter as Router, Routes, Route, Link} from 'react-router-dom';
import Dashboard from './pages/Dashboard';


function App() {
  const [count, setCount] = useState(0)

  return (
	<Router>
		<div className="min-h-screen bg-gray-900 text-white font-sans">
		{/* Nav Bar */}
		<nav className="p-4 bg-gray-800 border-b border-red-600 flex gap-6">
	<Link to="/" className="hover:text-red-500">Dashboard</Link>
	</nav>

	<main className="p-8">
		<Routes>
			<Route path="/" element={<Dashboard />} />
		</Routes>
	      </main>
	     </div>
	    </Router>
  );
}

export default App
