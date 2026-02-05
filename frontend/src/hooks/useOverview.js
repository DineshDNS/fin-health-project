import { useQuery } from "@tanstack/react-query";
import { fetchOverview } from "../api/overview";

export function useOverview() {
  return useQuery({
    queryKey: ["overview"],
    queryFn: fetchOverview,
    staleTime: 1000 * 60,      // 1 min
    retry: 1,
  });
}
