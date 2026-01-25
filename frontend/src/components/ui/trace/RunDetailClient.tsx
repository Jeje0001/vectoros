"use client"

import { useState } from "react"
import TraceTree from "@/components/ui/trace/TraceTree"
import StatsPanel from "@/components/ui/trace/StatsPanel"
import StepDetailsPanel from "@/components/ui/trace/StepDetailsPanel"
import { TraceNode } from "@/lib/traceTypes"
import { diagnoseRun } from "@/lib/diagnosis"
import { DiagnosisResult } from "@/lib/diagnose"
import { DiagnosisPanel } from "@/components/ui/DiagnosisPanel"
interface RunDetailClientProps {
  runId:string
  run: {
    input: string | null
    status: string
    model: string
    tokens: number | null
  }
  tree: TraceNode[]
}

export default function RunDetailClient({ runId,run, tree }: RunDetailClientProps) {
  const [selectedNode, setSelectedNode] = useState<TraceNode | null>(null)
  const [diagnosis, setDiagnosis] = useState<DiagnosisResult | null>(null)
  const [diagnosing, setDiagnosing] = useState(false)
  const [diagnosisError, setDiagnosisError] = useState<string | null>(null)
  console.log("API KEY:", process.env.NEXT_PUBLIC_VECTOROS_API_KEY)
  async function handleDiagnose() {
      setDiagnosing(true)
      setDiagnosisError(null)

      try {
        const result = await diagnoseRun(runId)
        setDiagnosis(result)
      } catch (err) {
        setDiagnosisError(
          err instanceof Error ? err.message : "Diagnosis failed"
        )
      } finally {
        setDiagnosing(false)
      }
    }
  return (
    <div className="p-6 h-screen flex flex-col">
      <div className="sticky top-0 bg-background z-10 pb-4 space-y-4">
        <h1 className="text-xl font-semibold">Run</h1>

        <div className="border rounded p-3">
          <div className="font-medium mb-1">Input</div>
          <pre className="text-xs bg-muted p-2 rounded whitespace-pre-wrap">
            {run.input ?? ""}
          </pre>
        </div>

        <div className="grid grid-cols-3 gap-4 text-sm">
          <div><strong>Status:</strong> {run.status}</div>
          <div><strong>Model:</strong> {run.model}</div>
          <div><strong>Tokens:</strong> {run.tokens ?? 0}</div>
        </div>
        <div className="flex items-center gap-3">
          <button
            onClick={handleDiagnose}
            disabled={diagnosing}
            className="px-3 py-1.5 text-sm border rounded-md hover:bg-muted disabled:opacity-50"
          >
            {diagnosing ? "Diagnosing…" : "Diagnose Run"}
          </button>

          {diagnosisError && (
            <span className="text-sm text-red-500">
              {diagnosisError}
            </span>
          )}
        </div>

        <StatsPanel tree={tree} />
      </div>

      <div className="flex-1 overflow-y-auto">
        <div className="grid grid-cols-[2fr_1fr] gap-4">
          <TraceTree tree={tree} onSelectNode={setSelectedNode} />
          {selectedNode !== null && <StepDetailsPanel node={selectedNode} />}
        </div>
      </div>
      {diagnosis && (
        <div className="mt-6">
          <DiagnosisPanel data={diagnosis} />
        </div>
      )}
    </div>
  )
}
