import { apiClient } from "./apiClient";

/**
 * Fetch Dashboard Overview
 * Backend endpoint: /api/overview/
 *
 * This function:
 * - Calls backend ONLY
 * - Normalizes DTO → UI shape
 * - Does NOT provide mock fallback
 */
export async function fetchDashboard() {
  const data = await apiClient("/api/overview/");

  if (!data || typeof data !== "object") {
    throw new Error("Invalid dashboard response");
  }

  return {
    last_updated: data.last_updated ?? "—",

    health_score: data.health_score,
    health_status: data.health_status,
    health_level: data.health_level,

    credit_status: data.credit_status,
    credit_level: data.credit_level,

    risk_status: data.risk_status,
    risk_level: data.risk_level,

    business: {
      industry: data.industry,
      bank_data: data.bank_data,
      gst_data: data.gst_data,
      financial_data: data.financial_data,
    },

    insights: Array.isArray(data.insights) ? data.insights : [],
  };
}
