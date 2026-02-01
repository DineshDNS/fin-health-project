import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import {
  getUserProfile,
  updateUserProfile,
  changePassword,
} from "../api/settingsApi";
import {
  FaUserCircle,
  FaLock,
  FaSignOutAlt,
} from "react-icons/fa";

export default function Settings() {
  const navigate = useNavigate();

  const [profile, setProfile] = useState(null);
  const [message, setMessage] = useState("");

  // Profile fields
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");

  // Password fields
  const [currentPassword, setCurrentPassword] = useState("");
  const [newPassword, setNewPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");

  useEffect(() => {
    getUserProfile()
      .then((res) => {
        setProfile(res.data);
        setUsername(res.data.username);
        setEmail(res.data.email || "");
      })
      .catch(() => navigate("/login"));
  }, [navigate]);

  const handleProfileUpdate = async () => {
    try {
      await updateUserProfile({ username, email });
      setMessage("Profile updated successfully");
    } catch {
      setMessage("Failed to update profile");
    }
  };

  const handlePasswordChange = async () => {
    if (newPassword !== confirmPassword) {
      setMessage("New passwords do not match");
      return;
    }

    try {
      await changePassword({
        current_password: currentPassword,
        new_password: newPassword,
      });

      setMessage("Password updated successfully");
      setCurrentPassword("");
      setNewPassword("");
      setConfirmPassword("");
    } catch {
      setMessage("Current password is incorrect");
    }
  };

  const handleLogout = () => {
    localStorage.clear();
    navigate("/login", { replace: true });
  };

  if (!profile) {
    return <p className="text-slate-600">Loading settings...</p>;
  }

  return (
    <div className="min-h-full p-8 rounded-3xl bg-gradient-to-br from-rose-100 via-pink-100 to-amber-100">

      {/* ================= ACCOUNT OVERVIEW ================= */}
      <div className="glass-card p-6 mb-10 flex items-center gap-6">
        <FaUserCircle className="text-5xl text-indigo-500" />
        <div>
          <p className="text-lg font-semibold text-slate-900">
            {profile.username}
          </p>
          <p className="text-sm text-slate-600">
            {profile.email || "No email provided"}
          </p>
          <span className="inline-block mt-2 px-3 py-1 text-xs rounded-full bg-emerald-100 text-emerald-700">
            Active Account
          </span>
        </div>
      </div>

      {/* ================= MAIN SETTINGS ================= */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 items-stretch">

        {/* ===== Edit Profile ===== */}
        <div className="glass-card p-6 flex flex-col">
          <h3 className="flex items-center gap-2 font-semibold text-slate-900 mb-6">
            <FaUserCircle className="text-indigo-500" />
            Edit Profile
          </h3>

          <div className="space-y-5">
            <div>
              <label className="text-sm text-slate-600">Username</label>
              <input
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                className="mt-2 w-full rounded-lg border-slate-300 bg-white/80
                           focus:ring-2 focus:ring-indigo-400"
              />
            </div>

            <div>
              <label className="text-sm text-slate-600">Email</label>
              <input
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="mt-2 w-full rounded-lg border-slate-300 bg-white/80
                           focus:ring-2 focus:ring-indigo-400"
              />
            </div>
          </div>

          {/* Button pinned to bottom */}
          <button
            onClick={handleProfileUpdate}
            className="mt-auto w-full py-3 rounded-xl
                       bg-gradient-to-r from-indigo-500 to-violet-500
                       text-white font-semibold
                       hover:opacity-90 transition"
          >
            Save Profile
          </button>
        </div>

        {/* ===== Change Password ===== */}
        <div className="glass-card p-6 flex flex-col">
          <h3 className="flex items-center gap-2 font-semibold text-slate-900 mb-6">
            <FaLock className="text-indigo-500" />
            Change Password
          </h3>

          <div className="space-y-5">
            <input
              type="password"
              placeholder="Current password"
              value={currentPassword}
              onChange={(e) => setCurrentPassword(e.target.value)}
              className="w-full rounded-lg border-slate-300 bg-white/80
                         focus:ring-2 focus:ring-indigo-400"
            />

            <input
              type="password"
              placeholder="New password"
              value={newPassword}
              onChange={(e) => setNewPassword(e.target.value)}
              className="w-full rounded-lg border-slate-300 bg-white/80
                         focus:ring-2 focus:ring-indigo-400"
            />

            <input
              type="password"
              placeholder="Confirm new password"
              value={confirmPassword}
              onChange={(e) => setConfirmPassword(e.target.value)}
              className="w-full rounded-lg border-slate-300 bg-white/80
                         focus:ring-2 focus:ring-indigo-400"
            />
          </div>

          {/* Button pinned to bottom */}
          <button
            onClick={handlePasswordChange}
            className="mt-auto w-full py-3 rounded-xl
                       bg-gradient-to-r from-indigo-500 to-violet-500
                       text-white font-semibold
                       hover:opacity-90 transition"
          >
            Update Password
          </button>
        </div>
      </div>

      {/* ================= SECURITY / LOGOUT ================= */}
      <div className="glass-card p-6 mt-10 border-l-4 border-rose-500">
        <h3 className="flex items-center gap-2 font-semibold text-slate-900 mb-2">
          <FaSignOutAlt />
          Security
        </h3>

        <p className="text-sm text-slate-600 mb-4">
          Logging out will end your current session on this device.
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

      {message && (
        <p className="mt-6 text-center text-sm text-slate-700">
          {message}
        </p>
      )}
    </div>
  );
}
