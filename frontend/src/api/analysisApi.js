import api from "./apiClient";

export const getAnalysisData = () => {
  return api.get("/analysis/");
};
