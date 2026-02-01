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
    <aside
      className="w-[280px] h-full flex flex-col
      bg-gradient-to-b from-slate-800 via-slate-900 to-indigo-900
      text-slate-200 shadow-2xl"
    >
      {/* ================= Brand ================= */}
      <div className="flex items-center gap-3 px-6 py-6">
        <div
          className="w-11 h-11 rounded-xl
          bg-gradient-to-br from-indigo-400 to-violet-600
          flex items-center justify-center
          text-white font-bold text-lg shadow-lg"
        >
          F
        </div>

        <span className="text-lg font-semibold text-white tracking-wide">
          FinHealth
        </span>
      </div>

      {/* Divider */}
      <div className="mx-6 border-t border-white/10" />

      {/* ================= Navigation ================= */}
      <nav className="flex-1 px-4 py-6 space-y-2">
        <NavLink to="/" end className={navClass}>
          <LayoutDashboard size={18} />
          Dashboard
        </NavLink>

        <NavLink to="/upload" className={navClass}>
          <Upload size={18} />
          Upload Files
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
      <div className="mx-6 border-t border-white/10" />

      {/* ================= Logout ================= */}
      <div className="px-6 py-6">
        <button
          onClick={handleLogout}
          className="flex items-center gap-3 text-sm font-medium
          text-rose-300 hover:text-rose-400 transition"
        >
          <LogOut size={18} />
          Logout
        </button>
      </div>
    </aside>
  );
}

/* ================= NavLink styles ================= */
const navClass = ({ isActive }) =>
  `flex items-center gap-4 px-5 py-3 rounded-xl text-sm font-medium transition-all
   ${
     isActive
       ? "bg-gradient-to-r from-indigo-400/90 to-violet-500/90 text-white shadow-lg"
       : "text-slate-300 hover:bg-white/10 hover:text-white"
   }`;
