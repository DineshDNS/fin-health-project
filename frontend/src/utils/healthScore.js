export function getHealthStatus(score) {
  if (score === null || score === undefined || isNaN(score)) {
    return {
      label: "Unknown",
      color: "text-slate-400",
      bg: "bg-slate-100",
    };
  }

  if (score >= 75) {
    return {
      label: "Healthy",
      color: "text-emerald-700",
      bg: "bg-emerald-50",
    };
  }

  if (score >= 50) {
    return {
      label: "Needs Attention",
      color: "text-amber-700",
      bg: "bg-amber-50",
    };
  }

  return {
    label: "At Risk",
    color: "text-red-700",
    bg: "bg-red-50",
  };
}
