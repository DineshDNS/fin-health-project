import { useLocation } from "react-router-dom";
import { useAuth } from "../../context/AuthContext";

const getTitleFromPath = (pathname) => {
  if (pathname === "/") return "Dashboard";
  if (pathname.startsWith("/upload")) return "Upload Files";
  if (pathname.startsWith("/documents")) return "Documents";
  if (pathname.startsWith("/analysis")) return "Analysis & Scores";
  if (pathname.startsWith("/settings")) return "Settings";
  return "Dashboard";
};

export default function Topbar() {
  const { pathname } = useLocation();
  const { user } = useAuth();

  const title = getTitleFromPath(pathname);
  const name = user?.name || "User";
  const initial = name.charAt(0).toUpperCase();

  return (
    <header
      className="h-16 px-6 flex items-center justify-between
      bg-white/70 backdrop-blur
      border-b border-white/40 shadow-sm"
    >
      {/* Page Title */}
      <h1 className="text-lg font-semibold text-slate-900">
        {title}
      </h1>

      {/* User Info */}
      <div className="flex items-center gap-3">
        <span className="text-sm text-slate-700 font-medium">
          {name}
        </span>

        <div
          className="w-9 h-9 rounded-full
          bg-gradient-to-br from-indigo-500 to-violet-600
          text-white flex items-center justify-center
          font-semibold shadow-md"
        >
          {initial}
        </div>
      </div>
    </header>
  );
}
