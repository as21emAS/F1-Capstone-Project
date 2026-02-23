import { BrowserRouter, Routes, Route } from "react-router-dom";
import Dashboard from "@pages/Dashboard";
import DashboardHome from "@pages/Dashboardhome";
import Simulator from "@pages/Simulator";
import DataCenter from "@pages/DataCenter";
import News from "@pages/News";
import NotFound from "@pages/NotFound";

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
	<Route path="*" element={<NotFound />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
