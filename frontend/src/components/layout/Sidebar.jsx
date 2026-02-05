import { NavLink } from "react-router-dom";

export default function Sidebar() {
  return (
    <aside className="fixed left-0 top-0 z-40 h-screen w-72 flex flex-col bg-sidebar-gradient text-white">
      {/* ============================= */}
      {/* TOP: BRAND / LOGO */}
      {/* ============================= */}
      <div className="flex items-center gap-4 px-6 py-6 border-b border-white/15">
        {/* Letter Logo */}
        <div className="h-12 w-12 rounded-xl bg-gradient-to-br from-white/90 to-white/60 text-slate-900 flex items-center justify-center font-extrabold text-lg shadow-md">
          SH
        </div>

        <div>
          <h1 className="text-lg font-bold tracking-wide">
            SME Health
          </h1>
          <p className="text-xs text-white/70">
            Financial Intelligence
          </p>
        </div>
      </div>

      {/* ============================= */}
      {/* MIDDLE: NAVIGATION */}
      {/* ============================= */}
      <nav className="flex-1 px-4 py-6 space-y-2">
        <SidebarLink to="/dashboard" label="Dashboard" icon={DashboardIcon} />
        <SidebarLink to="/documents" label="Documents" icon={DocumentIcon} />
        <SidebarLink to="/analysis" label="Analysis" icon={ChartIcon} />
      </nav>

      {/* ============================= */}
      {/* BOTTOM: ACTIONS */}
      {/* ============================= */}
      <div className="px-4 py-6 border-t border-white/15 space-y-2">
        <SidebarLink to="/settings" label="Settings" icon={SettingsIcon} />

        <button className="w-full flex items-center gap-3 px-4 py-3 rounded-xl text-base font-semibold text-white/80 hover:bg-white/15 transition">
          <LogoutIcon />
          Logout
        </button>
      </div>
    </aside>
  );
}

/* ============================= */
/* SIDEBAR LINK */
/* ============================= */

function SidebarLink({ to, label, icon: Icon }) {
  return (
    <NavLink
      to={to}
      className={({ isActive }) =>
        `
        flex items-center gap-3 px-4 py-3 rounded-xl
        text-base font-semibold tracking-wide
        transition
        ${
          isActive
            ? "bg-white/25 text-white shadow-sm"
            : "text-white/80 hover:bg-white/15"
        }
        `
      }
    >
      <Icon />
      {label}
    </NavLink>
  );
}

/* ============================= */
/* ICONS (INLINE SVG) */
/* ============================= */

function DashboardIcon() {
  return (
    <svg className="h-5 w-5" fill="none" stroke="currentColor" strokeWidth="2" viewBox="0 0 24 24">
      <rect x="3" y="3" width="7" height="7" />
      <rect x="14" y="3" width="7" height="7" />
      <rect x="14" y="14" width="7" height="7" />
      <rect x="3" y="14" width="7" height="7" />
    </svg>
  );
}

function DocumentIcon() {
  return (
    <svg className="h-5 w-5" fill="none" stroke="currentColor" strokeWidth="2" viewBox="0 0 24 24">
      <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" />
      <polyline points="14 2 14 8 20 8" />
    </svg>
  );
}

function ChartIcon() {
  return (
    <svg className="h-5 w-5" fill="none" stroke="currentColor" strokeWidth="2" viewBox="0 0 24 24">
      <line x1="12" y1="20" x2="12" y2="10" />
      <line x1="18" y1="20" x2="18" y2="4" />
      <line x1="6" y1="20" x2="6" y2="16" />
    </svg>
  );
}

function SettingsIcon() {
  return (
    <svg className="h-5 w-5" fill="none" stroke="currentColor" strokeWidth="2" viewBox="0 0 24 24">
      <circle cx="12" cy="12" r="3" />
      <path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1-2.83 2.83l-.06-.06A1.65 1.65 0 0 0 15 19.4a1.65 1.65 0 0 0-1 .6 1.65 1.65 0 0 0-.33 1.82V22a2 2 0 0 1-4 0v-.09a1.65 1.65 0 0 0-.33-1.82A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82-.33l-.06.06a2 2 0 0 1-2.83-2.83l.06-.06A1.65 1.65 0 0 0 4.6 15a1.65 1.65 0 0 0-.6-1.65 1.65 1.65 0 0 0-1.82-.33H2a2 2 0 0 1 0-4h.09a1.65 1.65 0 0 0 1.82-.33A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.6-1.82l-.06-.06a2 2 0 0 1 2.83-2.83l.06.06A1.65 1.65 0 0 0 9 4.6a1.65 1.65 0 0 0 1-.6A1.65 1.65 0 0 0 10.33 2H10a2 2 0 0 1 4 0h-.09a1.65 1.65 0 0 0 .33 1.82A1.65 1.65 0 0 0 15 4.6a1.65 1.65 0 0 0 1.82.33l.06-.06a2 2 0 0 1 2.83 2.83l-.06.06A1.65 1.65 0 0 0 19.4 9a1.65 1.65 0 0 0 .6 1.65 1.65 1.65 0 0 0 1.82.33H22a2 2 0 0 1 0 4h-.09a1.65 1.65 0 0 0-1.82.33A1.65 1.65 0 0 0 19.4 15z" />
    </svg>
  );
}

function LogoutIcon() {
  return (
    <svg className="h-5 w-5" fill="none" stroke="currentColor" strokeWidth="2" viewBox="0 0 24 24">
      <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4" />
      <polyline points="16 17 21 12 16 7" />
      <line x1="21" y1="12" x2="9" y2="12" />
    </svg>
  );
}
