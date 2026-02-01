import { useState } from "react";
import { useNavigate } from "react-router-dom";

export default function Settings() {
  const navigate = useNavigate();

  // -----------------------------
  // Local state (can be backend-driven later)
  // -----------------------------
  const [currency, setCurrency] = useState("INR");
  const [theme, setTheme] = useState("light");

  // -----------------------------
  // Actions
  // -----------------------------
  const handleLogout = () => {
    localStorage.removeItem("accessToken");
    localStorage.removeItem("refreshToken");
    navigate("/login", { replace: true });
  };

  const handleSavePreferences = () => {
    // Later: POST to backend
    alert("Preferences saved successfully");
  };

  return (
    <div className="min-h-full p-8 rounded-3xl bg-gradient-to-br from-rose-100 via-pink-100 to-amber-100">
      {/* Header */}
      <div className="mb-8">
        <h2 className="text-2xl font-semibold text-slate-900">
          Settings
        </h2>
        <p className="text-sm text-slate-600 mt-1">
          Manage your account and application preferences
        </p>
      </div>

      {/* Account Info */}
      <div className="glass-card p-6 mb-6">
        <h3 className="font-semibold text-slate-900 mb-4">
          Account Information
        </h3>

        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 text-sm">
          <div>
            <p className="text-slate-500">Username</p>
            <p className="font-medium text-slate-900">
              demo_user
            </p>
          </div>

          <div>
            <p className="text-slate-500">Email</p>
            <p className="font-medium text-slate-900">
              demo@company.com
            </p>
          </div>
        </div>
      </div>

      {/* Preferences */}
      <div className="glass-card p-6 mb-6">
        <h3 className="font-semibold text-slate-900 mb-4">
          Preferences
        </h3>

        <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
          {/* Currency */}
          <div>
            <label className="text-sm text-slate-600">
              Default Currency
            </label>
            <select
              value={currency}
              onChange={(e) => setCurrency(e.target.value)}
              className="mt-2 w-full rounded-lg border-slate-300"
            >
              <option value="INR">INR (₹)</option>
              <option value="USD">USD ($)</option>
              <option value="EUR">EUR (€)</option>
            </select>
          </div>

          {/* Theme */}
          <div>
            <label className="text-sm text-slate-600">
              Theme
            </label>
            <select
              value={theme}
              onChange={(e) => setTheme(e.target.value)}
              className="mt-2 w-full rounded-lg border-slate-300"
            >
              <option value="light">Light</option>
              <option value="dark">Dark</option>
              <option value="system">System Default</option>
            </select>
          </div>
        </div>

        <button
          onClick={handleSavePreferences}
          className="mt-6 px-6 py-2 rounded-xl
                     bg-indigo-600 text-white font-semibold
                     hover:bg-indigo-700 transition"
        >
          Save Preferences
        </button>
      </div>

      {/* Security */}
      <div className="glass-card p-6 border-l-4 border-rose-500">
        <h3 className="font-semibold text-slate-900 mb-2">
          Security
        </h3>
        <p className="text-sm text-slate-600 mb-4">
          Log out from this device or manage account security.
        </p>

        <button
          onClick={handleLogout}
          className="px-6 py-2 rounded-xl
                     bg-rose-600 text-white font-semibold
                     hover:bg-rose-700 transition"
        >
          Logout
        </button>
      </div>
    </div>
  );
}
