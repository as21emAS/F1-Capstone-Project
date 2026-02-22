import { BrowserRouter, Routes, Route } from "react-router-dom";
import Dashboard from "@pages/Dashboard";
import DashboardHome from "@pages/DashboardHome";
import Simulator from "@pages/Simulator";
import DataCenter from "@pages/DataCenter";
import News from "@pages/News";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Dashboard />}>
          <Route index element={<DashboardHome />} />
          <Route path="simulator" element={<Simulator />} />
          <Route path="data-center" element={<DataCenter />} />
          <Route path="news" element={<News />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App;