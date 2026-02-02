import api from "./apiClient";

export const getUserProfile = () => {
  return api.get("/users/me/");
};

export const updateUserProfile = (data) => {
  return api.patch("/users/update/", data);
};

export const changePassword = (data) => {
  return api.post("/users/change-password/", data);
};
