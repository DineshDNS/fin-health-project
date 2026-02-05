export async function fetchOverview() {
  const res = await fetch("http://127.0.0.1:8000/api/overview/", {
    credentials: "include", // future JWT/session safe
  });

  if (!res.ok) {
    throw new Error("Failed to load overview");
  }

  return res.json();
}
