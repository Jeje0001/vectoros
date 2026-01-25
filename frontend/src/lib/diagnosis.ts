
const BASE_URL = process.env.NEXT_PUBLIC_API_URL!

export async function diagnoseRun(runId: string) {
  const res = await fetch(
    `${BASE_URL}/runs/${runId}/diagnose`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-API-Key": process.env.NEXT_PUBLIC_VECTOROS_API_KEY!,
      },
    }
  )

  if (!res.ok) {
    const text = await res.text()
    throw new Error(text || "Diagnosis failed")
  }

  return res.json()
}