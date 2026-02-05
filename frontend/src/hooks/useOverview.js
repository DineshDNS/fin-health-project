import { useEffect, useState } from "react";
import { fetchOverview } from "../api/overview.api";

export default function useOverview() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    async function load() {
      try {
        const res = await fetchOverview();
        setData(res);
      } catch (err) {
        setError("Failed to load overview");
      } finally {
        setLoading(false);
      }
    }

    load();
  }, []);

  return { data, loading, error };
}
