import axios from "axios";

const API_BASE = "http://127.0.0.1:8000/api/documents";

export function getDocuments() {
  const token = localStorage.getItem("accessToken");

  return axios.get(`${API_BASE}/`, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });
}

export function getOverviewData() {
  const token = localStorage.getItem("accessToken");

  return axios.get(`${API_BASE}/overview/`, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });
}
