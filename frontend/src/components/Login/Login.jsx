import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import styles from "./Login.module.css";
import { loginUser } from "../../api/authApi";

function Login() {
  const navigate = useNavigate();

  const [form, setForm] = useState({
    username: "",
    password: "",
  });

  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleLogin = async () => {
    if (!form.username || !form.password) {
      setMessage("Username and password are required");
      return;
    }

    try {
      setLoading(true);
      setMessage("");

      const response = await loginUser({
        username: form.username,
        password: form.password,
      });

      localStorage.setItem("accessToken", response.data.access);
      localStorage.setItem("refreshToken", response.data.refresh);

      navigate("/upload");
    } catch (error) {
      setMessage(
        error.response?.data?.detail ||
        "Invalid username or password"
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className={styles.container}>
      <div className={styles.card}>
        <h2>Login</h2>

        {/* Username */}
        <div className={styles.field}>
          <label>Username</label>
          <div className={styles.inputRow}>
            <i className="far fa-user"></i>
            <input
              type="text"
              name="username"
              placeholder="Type your username"
              onChange={handleChange}
            />
          </div>
        </div>

        {/* Password */}
        <div className={styles.field}>
          <label>Password</label>
          <div className={styles.inputRow}>
            <i className="fas fa-lock"></i>
            <input
              type="password"
              name="password"
              placeholder="Type your password"
              onChange={handleChange}
            />
          </div>

          <div className={styles.forgot}>
            <Link to="/forgot-password">Forgot password?</Link>
          </div>
        </div>

        {message && <p className={styles.message}>{message}</p>}

        <button
          className={styles.btn}
          onClick={handleLogin}
          disabled={loading}
        >
          {loading ? "Logging in..." : "LOGIN"}
        </button>

        <p className={styles.footer}>
          Don&apos;t have an account? <Link to="/signup">Sign Up</Link>
        </p>
      </div>
    </div>
  );
}

export default Login;
