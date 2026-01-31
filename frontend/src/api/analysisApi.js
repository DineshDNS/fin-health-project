import axios from "axios";

const API_BASE_URL = "http://127.0.0.1:8000/api";

export function getAnalysisData() {
  const token = localStorage.getItem("accessToken");

  return axios.get(`${API_BASE_URL}/analysis/`, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });
}
