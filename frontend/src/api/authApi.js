import api from "./apiClient";

// SIGNUP
export const signupUser = (data) => {
  return api.post("/users/signup/", data);
};

// LOGIN

export const loginUser = (data) => {
  return api.post("/auth/login/", data);
};



