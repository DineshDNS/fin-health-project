import axios from "axios";

const API_BASE_URL = "http://127.0.0.1:8000/api";

export function signupUser(data) {
  return axios.post(`${API_BASE_URL}/auth/signup/`, data);
}

export function loginUser(data) {
  // ✅ FIXED endpoint
  return axios.post(`${API_BASE_URL}/auth/login/`, data);
}
