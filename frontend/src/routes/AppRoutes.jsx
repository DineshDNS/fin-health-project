import { Routes, Route, Navigate } from "react-router-dom";
import AppLayout from "../components/layout/AppLayout";
import Dashboard from "../pages/dashboard/Dashboard";
import Analysis from "../pages/analysis/Analysis";
import Documents from "../pages/documents/Documents";

export default function AppRoutes() {
  return (
    <Routes>
      <Route element={<AppLayout />}>
        {/* Dashboard */}
        <Route path="/" element={<Dashboard />} />
        <Route path="/analysis" element={<Analysis />} />
        <Route path="*" element={<Navigate to="/" replace />} />
        <Route path="/documents" element={<Documents />} />
      </Route>
    </Routes>
  );
}
