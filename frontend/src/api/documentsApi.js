import axios from "axios";

const API_BASE_URL = "http://127.0.0.1:8000/api";

export function getDocuments() {
  const token = localStorage.getItem("accessToken");

  return axios.get(`${API_BASE_URL}/documents/`, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });
}
