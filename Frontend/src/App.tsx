import { BrowserRouter, Routes, Route } from "react-router-dom";
import Layout from "@components/layout/Layout";
import DashboardHome from "@pages/Dashboardhome";
import Simulator from "@pages/Simulator";
import DataCenter from "@pages/DataCenter";
import Newsroom from "@pages/Newsroom";
import NotFound from "@pages/NotFound";
import ComponentDemo from "@pages/ComponentDemo";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<DashboardHome />} />
          <Route path="simulator" element={<Simulator />} />
          <Route path="data-center" element={<DataCenter />} />
          <Route path="newsroom" element={<Newsroom />} />
          <Route path="components" element={<ComponentDemo />} />
        </Route>
        <Route path="*" element={<NotFound />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
