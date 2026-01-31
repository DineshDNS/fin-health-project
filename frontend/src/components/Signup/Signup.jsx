import { useState } from "react";
import styles from "./Signup.module.css";
import { Link, useNavigate } from "react-router-dom";
import { signupUser } from "../../api/authApi";
import { FaUser, FaEnvelope, FaLock } from "react-icons/fa";

function Signup() {
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
    // Frontend validation
    if (!form.username || !form.password || !form.confirmPassword) {
      setMessage("Username and password are required");
      return;
    }

    if (form.password !== form.confirmPassword) {
      setMessage("Passwords do not match");
      return;
    }

    // Only send what backend expects
    const payload = {
      username: form.username,
      password: form.password,
    };

    try {
      setLoading(true);
      setMessage("");

      await signupUser(payload);

      setMessage("Signup successful. Redirecting to login...");
      setTimeout(() => navigate("/login"), 1500);
    } catch (error) {
      setMessage(
        error.response?.data?.error ||
        error.response?.data?.detail ||
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

        {/* Username */}
        <div className={styles.field}>
          <label>Username</label>
          <div className={styles.inputRow}>
            <FaUser className={styles.icon} />
            <input
              type="text"
              name="username"
              placeholder="Type your username"
              onChange={handleChange}
            />
          </div>
        </div>

        {/* Email (optional, not sent) */}
        <div className={styles.field}>
          <label>Email</label>
          <div className={styles.inputRow}>
            <FaEnvelope className={styles.icon} />
            <input
              type="email"
              name="email"
              placeholder="Type your email"
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
              placeholder="Type your password"
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
              placeholder="Confirm your password"
              onChange={handleChange}
            />
          </div>
        </div>

        {message && <p className={styles.message}>{message}</p>}

        <button
          className={styles.btn}
          onClick={handleSignup}
          disabled={loading}
        >
          {loading ? "Creating..." : "SIGN UP"}
        </button>

        <p className={styles.footer}>
          Already have an account? <Link to="/login">Login</Link>
        </p>
      </div>
    </div>
  );
}

export default Signup;
