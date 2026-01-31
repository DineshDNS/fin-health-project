import {
  LayoutDashboard,
  Upload,
  Folder,
  LineChart,
  Settings,
  LogOut,
} from "lucide-react";
import { NavLink, useNavigate } from "react-router-dom";
import { useAuth } from "../../context/AuthContext";

export default function Sidebar() {
  const { logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate("/login");
  };

  return (
    <aside className="w-[280px] h-full bg-slate-900 text-slate-200 flex flex-col">
      
      {/*Top: Title / Logo */}
      <div className="flex items-center gap-3 px-6 py-6">
        {/* Simple mark */}
        <div className="w-10 h-10 rounded-xl bg-indigo-600 flex items-center justify-center text-white font-bold">
          F
        </div>

        {/* Title */}
        <span className="text-lg font-semibold text-white">
          FinHealth
        </span>
      </div>

      {/* Divider */}
      <div className="mx-6 border-t border-slate-700/60" />

      {/* Middle: Navigation */}
      <nav className="flex-1 px-4 py-4 space-y-2">
        <NavLink to="/" end className={navClass}>
          <LayoutDashboard size={18} />
          Overview
        </NavLink>

        <NavLink to="/upload" className={navClass}>
          <Upload size={18} />
          Upload Financials
        </NavLink>

        <NavLink to="/documents" className={navClass}>
          <Folder size={18} />
          Documents
        </NavLink>

        <NavLink to="/analysis" className={navClass}>
          <LineChart size={18} />
          Analysis & Scores
        </NavLink>

        <NavLink to="/settings" className={navClass}>
          <Settings size={18} />
          Settings
        </NavLink>
      </nav>

      {/* Divider */}
      <div className="mx-6 border-t border-slate-700/60" />

      {/* Bottom: Logout */}
      <div className="px-10 py-8">
        <button
          onClick={handleLogout}
          className="flex items-center gap-3 text-sm font-medium text-red-400 hover:text-red-500 transition"
        >
          <LogOut size={18} />
          Logout
        </button>
      </div>
    </aside>
  );
}

const navClass = ({ isActive }) =>
  `flex items-center gap-4 px-5 py-3 rounded-xl text-sm font-medium transition
   ${
     isActive
       ? "bg-white text-slate-900 shadow-sm"
       : "text-slate-300 hover:bg-slate-700 hover:text-white"
   }`;
