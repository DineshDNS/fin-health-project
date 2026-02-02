import api from "./apiClient";

export const getDocuments = () => api.get("/ingestion/documents/");

export const deleteDocument = (id) =>
  api.delete(`/ingestion/documents/${id}/`);
