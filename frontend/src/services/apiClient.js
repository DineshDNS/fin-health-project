// src/services/apiClient.js

const API_BASE_URL = "http://localhost:8000"; // Django backend

export async function apiClient(endpoint, options = {}) {
  const token = localStorage.getItem("access_token");

  const headers = {
    "Content-Type": "application/json",
    ...(token && { Authorization: `Bearer ${token}` }),
    ...options.headers,
  };

  const response = await fetch(`${API_BASE_URL}${endpoint}`, {
    ...options,
    headers,
  });

  if (response.status === 401) {
    // Token expired or invalid
    localStorage.removeItem("access_token");
    localStorage.removeItem("refresh_token");

    // Optional: redirect to login
    window.location.href = "/login";
    throw new Error("Unauthorized");
  }

  if (!response.ok) {
    const error = await response.text();
    throw new Error(error || "API Error");
  }

  return response.json();
}
