export function formatNumber(value) {
  if (value === null || value === undefined || isNaN(value)) {
    return "—";
  }

  return new Intl.NumberFormat("en-IN").format(value);
}
