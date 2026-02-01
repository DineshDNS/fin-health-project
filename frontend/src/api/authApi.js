import axios from "axios";

const API_BASE_URL = "http://127.0.0.1:8000/api";

// SIGNUP
export function signupUser(data) {
  return axios.post(`${API_BASE_URL}/users/signup/`, data);
}

// LOGIN (JWT)
export function loginUser(data) {
  return axios.post(`${API_BASE_URL}/auth/login/`, data);
}
