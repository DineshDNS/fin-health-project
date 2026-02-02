import api from "./apiClient";

export const uploadFinancialDocument = (formData) => {
  return api.post("/ingestion/upload/", formData, {
    headers: {
      "Content-Type": "multipart/form-data",
    },
  });
};
