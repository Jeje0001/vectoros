import { RunSummary } from "@/lib/types"

function formatTime(iso: string | null) {
  if (!iso) return "Unknown time"
  const diff = Date.now() - new Date(iso).getTime()
  const mins = Math.floor(diff / 60000)
  if (mins < 60) return `${mins}m ago`
  const hours = Math.floor(mins / 60)
  return `${hours}h ago`
}

export default function SidebarItem({ run }: { run: RunSummary }) {
  const inputPreview = run.input
    ? run.input.slice(0, 30)
    : "No input"

  const shortId = run.run_id.slice(-4)

  return (
    <div className="p-3 border-b cursor-pointer hover:bg-muted">
      <div className="font-medium">{inputPreview}</div>
      <div className="text-xs text-muted-foreground">
        {formatTime(run.created_at)} • ...{shortId}
      </div>
      <div className="text-xs">
        {run.status}
      </div>
    </div>
  )
}
