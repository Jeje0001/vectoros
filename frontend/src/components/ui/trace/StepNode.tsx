import { TraceNode } from "@/lib/traceTypes"
interface StepNodeProps {
  node: TraceNode
  depth: number
  isExpanded: boolean
  isOnErrorPath: boolean
  isOnSlowPath: boolean
  isOnExpensivePath: boolean
  onToggle: () => void
  onSelect: () => void
  isSelected: boolean

}

export default function StepNode({
  node,
  depth,
  isExpanded,
  isOnErrorPath,
  isOnSlowPath,
  isOnExpensivePath,
  onToggle,
  onSelect,
  isSelected
}: StepNodeProps) {

  const hasError = node.error !== null
  const isSlow = node.flags?.is_slow_step === true
  const isExpensive = node.flags?.is_expensive_step === true
  const childCount = node.children.length

  // ---------- Visual State ----------
  let accent = "border-border"
  let bg = "bg-transparent"

  if (isOnErrorPath) {
    accent = "border-red-500"
    bg = "bg-red-500/10"
  } else if (isOnSlowPath) {
    accent = "border-yellow-400"
    bg = "bg-yellow-400/10"
  } else if (isOnExpensivePath) {
    accent = "border-orange-400"
    bg = "bg-orange-400/10"
  }

  return (
      <div
      onClick={onSelect}
      className={`
        flex items-center gap-3 text-sm
        py-2 pl-3 pr-2
        border-l-2 ${accent}
        ${bg}
        rounded-md
        cursor-pointer
        transition-colors
        ${isSelected ? "ring-2 ring-primary/60" : ""}
        hover:bg-muted/40
      `}
    >


      {/* Expand / Collapse */}
      {childCount > 0 && (
        <button
          onClick={onToggle}
          className="text-xs w-4 text-muted-foreground hover:text-foreground transition"
        >
          {isExpanded ? "▼" : "▶"}
        </button>
      )}

      {/* Step Type */}
      <span className="font-mono min-w-[90px] text-muted-foreground">
        {node.type}
      </span>

      {/* Tokens */}
      <span className={`text-xs min-w-[70px] ${isExpensive ? "text-orange-400 font-semibold" : "text-muted-foreground"}`}>
        {node.tokens} tok
      </span>

      {/* Latency */}
      <span className={`text-xs min-w-[70px] ${isSlow ? "text-yellow-400 font-semibold" : "text-muted-foreground"}`}>
        {node.latency} ms
      </span>

      {/* Children */}
      <span className="text-xs text-muted-foreground min-w-[80px]">
        {childCount} children
      </span>

      {/* Error */}
      {hasError && (
        <span className="text-xs text-red-400 font-semibold">
          ERROR
        </span>
      )}
    </div>
  )
}
