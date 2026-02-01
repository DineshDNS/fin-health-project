import axios from "axios";

const API_BASE_URL = "http://127.0.0.1:8000/api";

export function uploadFinancialDocument(formData) {
  const token = localStorage.getItem("accessToken");

  return axios.post(`${API_BASE_URL}/upload/`, formData, {
    headers: {
      Authorization: token ? `Bearer ${token}` : "",
      "Content-Type": "multipart/form-data",
    },
  });
}
