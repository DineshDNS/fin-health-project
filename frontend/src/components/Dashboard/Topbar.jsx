import { useLocation } from "react-router-dom";
import { useAuth } from "../../context/AuthContext";

const titles = {
  "/": "Overview",
  "/upload": "Upload Financials",
  "/documents": "Documents",
  "/analysis": "Analysis & Scores",
  "/settings": "Settings",
};

export default function Topbar() {
  const { pathname } = useLocation();
  const { user } = useAuth();

  const title = titles[pathname] || "Overview";
  const name = user?.name || "User";
  const initial = name.charAt(0).toUpperCase();

  return (
    <header className="h-16 bg-white border-b border-slate-300 flex items-center justify-between px-6">
      <h1 className="text-base font-semibold">{title}</h1>

      <div className="flex items-center gap-3">
        <span className="text-sm">{name}</span>
        <div className="w-9 h-9 rounded-full bg-indigo-600 text-white flex items-center justify-center font-semibold">
          {initial}
        </div>
      </div>
    </header>
  );
}
