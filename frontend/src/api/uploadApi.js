import axios from "axios";

const API_BASE_URL = "http://127.0.0.1:8000/api";

export function uploadFinancialFile(file) {
  const token = localStorage.getItem("accessToken");

  const formData = new FormData();
  formData.append("file", file); 

  return axios.post(
    `${API_BASE_URL}/upload/`,
    formData,
    {
      headers: {
        Authorization: `Bearer ${token}`, 
      },
    }
  );
}
