import { TraceNode } from "@/lib/traceTypes"

export default function StepDetailsPanel({ node }: { node: TraceNode }) {
  return (
    <div className="border rounded-lg p-4 text-sm space-y-3">
      <div className="font-semibold">Step Details</div>

      <div><b>Type:</b> {node.type}</div>
      <div><b>Tokens:</b> {node.tokens}</div>
      <div><b>Latency:</b> {node.latency} ms</div>

      <div>
        <b>Flags:</b>
        <ul className="ml-4 list-disc text-muted-foreground">
          <li>Slow step: {String(node.flags?.is_slow_step === true)}</li>
          <li>Expensive step: {String(node.flags?.is_expensive_step === true)}</li>
        </ul>
      </div>

      <div>
        <b>Error:</b>
        <pre className="bg-muted rounded p-2 text-xs overflow-auto">
          {node.error ?? "—"}
        </pre>
      </div>
    </div>
  )
}
