import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import styles from "./Signup.module.css";
import { signupUser } from "../../api/authApi";
import { FaUser, FaEnvelope, FaLock } from "react-icons/fa";

export default function Signup() {
  const navigate = useNavigate();

  const [form, setForm] = useState({
    username: "",
    email: "",
    password: "",
    confirmPassword: "",
  });

  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSignup = async () => {
    if (!form.username || !form.password || !form.confirmPassword) {
      setMessage("Username and password are required");
      return;
    }

    if (form.password !== form.confirmPassword) {
      setMessage("Passwords do not match");
      return;
    }

    try {
      setLoading(true);
      setMessage("");

      await signupUser({
        username: form.username,
        email: form.email,
        password: form.password,
      });

      setMessage("Signup successful. Redirecting to login...");
      setTimeout(() => navigate("/login"), 1000);
    } catch (err) {
      setMessage(
        err.response?.data?.detail ||
        err.response?.data?.error ||
        "Signup failed"
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className={styles.container}>
      <div className={styles.card}>
        <h2>Sign Up</h2>

        <form
          onSubmit={(e) => {
            e.preventDefault();
            handleSignup();
          }}
        >
          {/* Username */}
          <div className={styles.field}>
            <label>Username</label>
            <div className={styles.inputRow}>
              <FaUser className={styles.icon} />
              <input
                type="text"
                name="username"
                placeholder="Enter your username"
                value={form.username}
                onChange={handleChange}
              />
            </div>
          </div>

          {/* Email */}
          <div className={styles.field}>
            <label>Email</label>
            <div className={styles.inputRow}>
              <FaEnvelope className={styles.icon} />
              <input
                type="email"
                name="email"
                placeholder="Enter your email address"
                value={form.email}
                onChange={handleChange}
              />
            </div>
          </div>

          {/* Password */}
          <div className={styles.field}>
            <label>Password</label>
            <div className={styles.inputRow}>
              <FaLock className={styles.icon} />
              <input
                type="password"
                name="password"
                placeholder="Create a password"
                value={form.password}
                onChange={handleChange}
              />
            </div>
          </div>

          {/* Confirm Password */}
          <div className={styles.field}>
            <label>Confirm Password</label>
            <div className={styles.inputRow}>
              <FaLock className={styles.icon} />
              <input
                type="password"
                name="confirmPassword"
                placeholder="Re-enter your password"
                value={form.confirmPassword}
                onChange={handleChange}
              />
            </div>
          </div>

          {message && <p className={styles.message}>{message}</p>}

          <button type="submit" className={styles.btn} disabled={loading}>
            {loading ? "Creating..." : "SIGN UP"}
          </button>
        </form>

        <p className={styles.footer}>
          Already have an account? <Link to="/login">Login</Link>
        </p>
      </div>
    </div>
  );
}
