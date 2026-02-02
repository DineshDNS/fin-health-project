import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import {
  getUserProfile,
  updateUserProfile,
  changePassword,
} from "../api/settingsApi";
import { FaUserCircle, FaLock, FaSignOutAlt } from "react-icons/fa";

export default function Settings() {
  const navigate = useNavigate();

  const [profile, setProfile] = useState(null);
  const [message, setMessage] = useState("");

  // ✅ always strings (controlled inputs)
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");

  const [currentPassword, setCurrentPassword] = useState("");
  const [newPassword, setNewPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");

  useEffect(() => {
    getUserProfile()
      .then((res) => {
        setProfile(res.data);
        setUsername(res.data.username || "");
        setEmail(res.data.email || "");
      })
      .catch((err) => {
        console.error(err);
        if (err.response?.status === 401) {
          localStorage.clear();
          navigate("/login", { replace: true });
        } else {
          setMessage("Failed to load profile");
        }
      });
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
    if (!currentPassword || !newPassword || !confirmPassword) {
      setMessage("Please fill all password fields");
      return;
    }

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
    <div className="min-h-full p-10 rounded-3xl bg-gradient-to-br from-rose-100 via-pink-100 to-amber-100">

      <div className="glass-card p-8 mb-12 flex items-center gap-6">
        <FaUserCircle className="text-6xl text-indigo-500" />
        <div>
          <p className="text-xl font-semibold text-slate-900">{profile.username}</p>
          <p className="text-sm text-slate-600">
            {profile.email || "No email provided"}
          </p>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-10 items-stretch">

        <div className="glass-card p-8 flex flex-col min-h-[440px]">
          <h3 className="flex items-center gap-2 font-semibold mb-8">
            <FaUserCircle /> Edit Profile
          </h3>

          <div className="space-y-6">
            <input
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              className="w-full px-4 py-3 rounded-xl"
              placeholder="Username"
            />
            <input
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="w-full px-4 py-3 rounded-xl"
              placeholder="Email"
            />
          </div>

          <button
            onClick={handleProfileUpdate}
            className="mt-auto py-4 rounded-2xl bg-indigo-600 text-white font-semibold"
          >
            Save Profile
          </button>
        </div>

        <div className="glass-card p-8 flex flex-col min-h-[440px]">
          <h3 className="flex items-center gap-2 font-semibold mb-8">
            <FaLock /> Change Password
          </h3>

          <div className="space-y-6">
            <input
              type="password"
              value={currentPassword}
              onChange={(e) => setCurrentPassword(e.target.value)}
              className="w-full px-4 py-3 rounded-xl"
              placeholder="Current password"
            />
            <input
              type="password"
              value={newPassword}
              onChange={(e) => setNewPassword(e.target.value)}
              className="w-full px-4 py-3 rounded-xl"
              placeholder="New password"
            />
            <input
              type="password"
              value={confirmPassword}
              onChange={(e) => setConfirmPassword(e.target.value)}
              className="w-full px-4 py-3 rounded-xl"
              placeholder="Confirm new password"
            />
          </div>

          <button
            onClick={handlePasswordChange}
            className="mt-auto py-4 rounded-2xl bg-indigo-600 text-white font-semibold"
          >
            Update Password
          </button>
        </div>
      </div>

      <div className="glass-card p-8 mt-12 border-l-4 border-rose-500">
        <button
          onClick={handleLogout}
          className="px-8 py-3 rounded-2xl bg-rose-600 text-white font-semibold"
        >
          <FaSignOutAlt /> Logout
        </button>
      </div>

      {message && <p className="mt-6 text-center">{message}</p>}
    </div>
  );
}
