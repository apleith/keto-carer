import { Routes, Route, Navigate } from "react-router-dom";
import Layout from "@/components/Layout";
import Dashboard from "@/pages/Dashboard";
import MealPlanning from "@/pages/MealPlanning";
import GroceryList from "@/pages/GroceryList";
import Progress from "@/pages/Progress";
import Medications from "@/pages/Medications";
import WaterTracking from "@/pages/WaterTracking";
import Settings from "@/pages/Settings";

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<Layout />}>
        <Route index element={<Navigate to="/dashboard" replace />} />
        <Route path="dashboard" element={<Dashboard />} />
        <Route path="meals" element={<MealPlanning />} />
        <Route path="grocery" element={<GroceryList />} />
        <Route path="progress" element={<Progress />} />
        <Route path="medications" element={<Medications />} />
        <Route path="water" element={<WaterTracking />} />
        <Route path="settings" element={<Settings />} />
      </Route>
    </Routes>
  );
}
