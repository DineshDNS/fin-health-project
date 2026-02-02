import api from "./apiClient";

export const getOverviewData = () => {
  return api.get("/overview/");
};