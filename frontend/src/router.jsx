import { createBrowserRouter } from "react-router-dom";
import DashboardLayout from "./layouts/DashboardLayout";
import Login from "./pages/Login";
import Signup from "./pages/Signup";
import Overview from "./pages/Overview";
import UploadFinancials from "./pages/Upload";
import Documents from "./pages/Documents";
import Analysis from "./pages/Analysis";
import Settings from "./pages/Settings";
import { AuthProvider } from "./context/AuthContext";

export const router = createBrowserRouter([
  {
    path: "/login",
    element: (
      <AuthProvider>
        <Login />
      </AuthProvider>
    ),
  },
  {
    path: "/signup",
    element: (
      <AuthProvider>
        <Signup />
      </AuthProvider>
    ),
  },
  {
    path: "/",
    element: (
      <AuthProvider>
        <DashboardLayout />
      </AuthProvider>
    ),
    children: [
      { index: true, element: <Overview /> },
      { path: "upload", element: <UploadFinancials /> },
      { path: "documents", element: <Documents /> },
      { path: "analysis", element: <Analysis /> },
      { path: "settings", element: <Settings /> },
    ],
  },
]);
