import {
  LayoutDashboard,
  Upload,
  Folder,
  LineChart,
  Settings,
  LogOut,
} from "lucide-react";
import { NavLink } from "react-router-dom";

export default function Sidebar() {
  return (
    <aside className="w-[280px] h-full bg-gradient-to-b from-slate-900 to-slate-800 text-slate-200 flex flex-col">
      
      {/* Logo */}
      <div className="flex items-center gap-3 px-6 py-6">
        <div className="w-10 h-10 rounded-xl bg-indigo-600 flex items-center justify-center text-white font-bold">
          F
        </div>
        <span className="text-lg font-semibold text-white">
          FinHealth
        </span>
      </div>

      {/* Navigation */}
      <nav className="flex-1 px-4 space-y-2">
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

      {/* Logout */}
      <div className="px-6 py-6">
        <button className="flex items-center gap-3 text-sm font-medium text-red-400 hover:text-red-500">
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
       ? "bg-white text-slate-900 shadow"
       : "text-slate-300 hover:bg-slate-700 hover:text-white"
   }`;
