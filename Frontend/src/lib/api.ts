const BASE_URL = process.env.NEXT_PUBLIC_API_URL!;

export async function getRuns() {
  const res = await fetch(`${BASE_URL}/runs`);

  if (!res.ok) {
    throw new Error("Failed to fetch runs");
  }

  return res.json();
}

export async function getRunById(id: string) {
  const res = await fetch(`${BASE_URL}/runs/${id}`);

  if (!res.ok) {
    throw new Error("Failed to fetch run");
  }

  return res.json();
}
