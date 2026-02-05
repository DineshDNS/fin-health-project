import api from "./axios";

export async function fetchOverview() {
  const response = await api.get("/api/overview/");
  return response.data;
}
