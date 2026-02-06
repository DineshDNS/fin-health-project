import axios from "axios";

/*
  Central API client (FINAL)
  -------------------------
  - Supports JSON requests
  - Supports FormData uploads
  - Automatically sets correct Content-Type
*/

const api = axios.create({
  baseURL: "http://127.0.0.1:8000/api",
  withCredentials: false,
});

// Attach JWT token if present
api.interceptors.request.use((config) => {
  const token = localStorage.getItem("access_token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }

  // IMPORTANT:
  // Do NOT set Content-Type here
  // Axios will set it automatically based on payload
  return config;
});

export default api;
