import { createBrowserRouter } from "react-router-dom";

/* Layout */
import DashboardLayout from "./layouts/DashboardLayout";

/* Auth pages */
import LoginPage from "./pages/Login";
import SignupPage from "./pages/signup";

/* Dashboard pages */
import Overview from "./pages/Overview";
import Upload from "./pages/Upload";
import Documents from "./pages/Documents";
import Analysis from "./pages/Analysis";
import Settings from "./pages/Settings";

export const router = createBrowserRouter([
  /* ---------------- AUTH ROUTES (NO SIDEBAR) ---------------- */
  {
    path: "/login",
    element: <LoginPage />,
  },
  {
    path: "/signup",
    element: <SignupPage />,
  },

  /* ---------------- DASHBOARD ROUTES (WITH SIDEBAR) ---------------- */
  {
    path: "/",
    element: <DashboardLayout />,
    children: [
      { index: true, element: <Overview /> },
      { path: "upload", element: <Upload /> },
      { path: "documents", element: <Documents /> },
      { path: "analysis", element: <Analysis /> },
      { path: "settings", element: <Settings /> },
    ],
  },
]);
