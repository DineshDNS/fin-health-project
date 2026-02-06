import { useQuery } from "@tanstack/react-query";
import { fetchOverview } from "../api/overview";

export function useOverview() {
  return useQuery({
    queryKey: ["overview"],
    queryFn: fetchOverview,

    // DO NOT CACHE LONG
    staleTime: 0,

    //ALWAYS REFRESH WHEN USER RETURNS
    refetchOnWindowFocus: true,

    // AUTO REFRESH IN BACKGROUND
    refetchInterval: 2000, // every 5 seconds

    retry: 1,
  });
}
