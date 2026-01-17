import { TraceNode } from "@/lib/traceTypes"

interface Stats {
  totalSteps: number
  totalTokens: number
  totalLatency: number
  errorCount: number
  maxDepth: number
}

function computeStats(node: TraceNode, depth: number): Stats {
    const stats: Stats = {
    totalSteps: 1,
    totalTokens: node.tokens,
    totalLatency: node.latency,
    errorCount: node.error ? 1 : 0,
    maxDepth: depth
  }

  for (const child of node.children) {
    const childStats = computeStats(child, depth + 1)

    stats.totalSteps += childStats.totalSteps
    stats.totalTokens += childStats.totalTokens
    stats.totalLatency += childStats.totalLatency
    stats.errorCount += childStats.errorCount
    stats.maxDepth = Math.max(stats.maxDepth, childStats.maxDepth)
  }

  return stats
}

export default function StatsPanel({ tree }: { tree: TraceNode[] }) {
  const summary: Stats = {
    totalSteps: 0,
    totalTokens: 0,
    totalLatency: 0,
    errorCount: 0,
    maxDepth: 0
  }

  for (const node of tree) {
    const stats = computeStats(node, 0)

    summary.totalSteps += stats.totalSteps
    summary.totalTokens += stats.totalTokens
    summary.totalLatency += stats.totalLatency
    summary.errorCount += stats.errorCount
    summary.maxDepth = Math.max(summary.maxDepth, stats.maxDepth)
  }

  return (
  <div className="grid grid-cols-5 gap-3 mb-4">
    <Stat label="Steps" value={summary.totalSteps} />
    <Stat label="Tokens" value={summary.totalTokens} />
    <Stat label="Latency" value={`${summary.totalLatency} ms`} />
    <Stat label="Errors" value={summary.errorCount} highlight={summary.errorCount > 0} />
    <Stat label="Max Depth" value={summary.maxDepth} />
  </div>
)

}

function Stat({
  label,
  value,
  highlight = false
}: {
  label: string
  value: string | number
  highlight?: boolean
}) {
  return (
    <div
      className={`
        rounded-lg border px-4 py-3
        bg-card shadow-sm
        flex flex-col items-center justify-center
        transition-all
        ${highlight ? "border-red-500/50 bg-red-500/10" : "border-border"}
      `}
    >
      <div className="text-xs text-muted-foreground uppercase tracking-wide">
        {label}
      </div>
      <div className="text-lg font-semibold mt-1">
        {value}
      </div>
    </div>
  )
}

