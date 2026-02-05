import { apiClient } from "./client"

export async function fetchOverview() {
  const res = await apiClient.get("/api/overview/")
  return res.data.data
}