import Sidebar from "./Sidebar";
import { Outlet } from "react-router-dom";

export default function AppLayout() {
  return (
    <div className="h-screen w-full bg-app-gradient">
      {/* FIXED SIDEBAR */}
      <Sidebar />

      {/* MAIN AREA */}
      <div className="ml-72 h-screen flex flex-col">
        {/* STICKY HEADER */}
        <header className="sticky top-0 z-30">
          <div className="relative bg-gradient-to-r from-rose-300 via-rose-400 to-pink-400">
            <div className="absolute inset-0 bg-black/10 pointer-events-none" />

            <div className="relative px-6 py-4">
              <h1 className="text-base font-semibold text-slate-900">
                SME Financial Health Platform
              </h1>
              <p className="text-[11px] text-slate-800/80">
                Monitor, analyze, and improve business health
              </p>
            </div>

            {/* SEPARATOR */}
            <div className="relative h-[3px] overflow-hidden">
              <div className="absolute inset-0 bg-gradient-to-r from-transparent via-rose-600 to-transparent" />
              <div className="absolute inset-0 bg-gradient-to-r from-transparent via-rose-500/70 to-transparent animate-separator" />
            </div>
          </div>
        </header>

        {/* SCROLLABLE BODY */}
        <main className="flex-1 overflow-y-auto bg-app-gradient">
          <div className="p-6">
            <Outlet />
          </div>
        </main>
      </div>
    </div>
  );
}
