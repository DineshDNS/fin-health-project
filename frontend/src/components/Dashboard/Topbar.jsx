import { useLocation } from "react-router-dom";

const titles = {
  "/": "Overview",
  "/upload": "Upload Financials",
  "/documents": "Documents",
  "/analysis": "Analysis & Scores",
  "/settings": "Settings",
};

export default function Topbar() {
  const { pathname } = useLocation();
  const title = titles[pathname] || "Overview";

  return (
    <header className="h-16 bg-white border-b border-slate-200 flex items-center justify-between px-6">
      <h1 className="text-base font-semibold text-slate-800">
        {title}
      </h1>

      <div className="flex items-center gap-4">
        <span className="text-sm text-slate-600">
          Dinesh
        </span>
        <div className="w-9 h-9 rounded-full bg-slate-200" />
      </div>
    </header>
  );
}
