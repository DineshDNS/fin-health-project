export function formatCurrency(value, options = {}) {
  if (value === null || value === undefined || isNaN(value)) {
    return "—";
  }

  const {
    locale = "en-IN",
    currency = "INR",
    minimumFractionDigits = 0,
    maximumFractionDigits = 2,
  } = options;

  return new Intl.NumberFormat(locale, {
    style: "currency",
    currency,
    minimumFractionDigits,
    maximumFractionDigits,
  }).format(value);
}
