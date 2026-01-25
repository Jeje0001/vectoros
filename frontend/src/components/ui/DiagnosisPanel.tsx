import { DiagnosisResult } from "@/lib/diagnose";

export function DiagnosisPanel({ data }: { data: DiagnosisResult }) {
  return (
    <div className="border rounded p-4 space-y-4">
      <div>
        <h3 className="font-semibold">Root Cause</h3>
        <p>{data.root_cause}</p>
      </div>

      <div>
        <h3 className="font-semibold">Explanation</h3>
        <p>{data.explanation}</p>
      </div>

      <div>
        <h3 className="font-semibold">Suggested Fix</h3>
        <p>{data.suggested_fix}</p>
      </div>

      <div className="pt-2 border-t">
        <p>Reliability: {data.reliability_score}</p>
        <p>Tokens: {data.cost_analysis.total_tokens}</p>
        <p>Estimated Cost: ${data.cost_analysis.estimated_cost_usd ?? "N/A"}</p>

        {data.cost_analysis.expensive_steps.length > 0 && (
          <div>
            <p className="font-medium">Expensive Steps</p>
            <ul className="list-disc ml-4">
              {data.cost_analysis.expensive_steps.map((s) => (
                <li key={s}>{s}</li>
              ))}
            </ul>
          </div>
        )}
      </div>
    </div>
  );
}