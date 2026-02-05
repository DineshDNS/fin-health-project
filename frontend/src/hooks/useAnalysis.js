import { useQuery } from "@tanstack/react-query";
import axios from "axios";

const fetchAnalysis = async () => {
  const res = await axios.get("/api/analysis/");
  return res.data;
};

export function useAnalysis() {
  return useQuery({
    queryKey: ["analysis"],
    queryFn: fetchAnalysis,
    staleTime: 1000 * 60 * 5,
    cacheTime: 1000 * 60 * 10,
    retry: 1,
    refetchOnWindowFocus: false,
    select: (data) => data ?? null,
  });
}
