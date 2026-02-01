import axios from "axios";

const API_BASE_URL = "http://127.0.0.1:8000/api";

function authHeaders() {
  return {
    Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
  };
}

export function getUserProfile() {
  return axios.get(`${API_BASE_URL}/users/me/`, {
    headers: authHeaders(),
  });
}

export function updateUserProfile(data) {
  return axios.patch(
    `${API_BASE_URL}/users/update/`,
    data,
    { headers: authHeaders() }
  );
}

export function changePassword(data) {
  return axios.post(
    `${API_BASE_URL}/users/change-password/`,
    data,
    { headers: authHeaders() }
  );
}
