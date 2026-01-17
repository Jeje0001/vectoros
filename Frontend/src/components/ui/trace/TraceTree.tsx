"use client"

import { useState } from "react"
import StepNode from "./StepNode"
import { TraceNode } from "@/lib/traceTypes"

export default function TraceTree({
  tree,
  onSelectNode
}: {
  tree: TraceNode[]
  onSelectNode: (node: TraceNode) => void
}) {

  const [expanded, setExpanded] = useState<Set<string>>(
    new Set(["root"])
  )
  const [selectedNode, setSelectedNode] = useState<TraceNode | null>(null)


  function toggleNode(id: string) {
    setExpanded(function (previousExpanded) {
      const nextExpanded = new Set(previousExpanded)

      if (nextExpanded.has(id)) {
        nextExpanded.delete(id)
      } else {
        nextExpanded.add(id)
      }

      return nextExpanded
    })
  }

function nodeContainsError(node: TraceNode): boolean {
  if (node.error !== null) {
    return true
  }

  for (const child of node.children) {
    if (nodeContainsError(child)) {
      return true
    }
  }

  return false
}


function renderNode(node: TraceNode, depth: number) {
  const isExpanded = expanded.has(node.id)
  const isOnErrorPath = nodeContainsError(node)
  const isOnSlowPath = nodeContainsSlow(node)
  const isOnExpensivePath = nodeContainsExpensive(node)
  const isSelected = selectedNode !== null && selectedNode.id === node.id


  return (
    <div key={node.id}>
      <StepNode
        node={node}
        depth={depth}
        isExpanded={isExpanded}
        isOnErrorPath={isOnErrorPath}
        isOnSlowPath={isOnSlowPath}
        isOnExpensivePath={isOnExpensivePath}
        isSelected={isSelected}
        onToggle={function () {
          toggleNode(node.id)
        }}
        onSelect={function () {
          onSelectNode(node)
        }}
      />




      {isExpanded === true && (
        <div>
          {node.children.map(function (child) {
            return renderNode(child, depth + 1)
          })}
        </div>
      )}
    </div>
  )
}
function nodeContainsSlow(node: TraceNode): boolean {
  if (node.flags?.is_slow_step === true) {
    return true
  }

  for (const child of node.children) {
    if (nodeContainsSlow(child)) {
      return true
    }
  }

  return false
}

function nodeContainsExpensive(node: TraceNode): boolean {
  if (node.flags?.is_expensive_step === true) {
    return true
  }

  for (const child of node.children) {
    if (nodeContainsExpensive(child)) {
      return true
    }
  }

  return false
}

    if (tree.length === 0) {
    return (
      <div className="mt-4 border rounded p-4 text-sm text-muted-foreground">
        No execution steps recorded for this run.
      </div>
    )
  }


  return (
  <div className="relative mt-4 rounded-xl border border-border bg-card shadow-sm">
    <div className="px-4 py-3 border-b border-border flex items-center justify-between">
      <div className="font-semibold text-sm tracking-tight">Trace</div>
      <div className="text-xs text-muted-foreground">
        Execution Tree
      </div>
    </div>

    <div className="px-3 py-2 font-mono text-[13px] leading-relaxed">
      <div className="relative pl-3">
        <div className="absolute left-0 top-0 bottom-0 w-px bg-border" />

        {tree.map(function (node) {
          return renderNode(node, 0)
        })}
      </div>
    </div>
  </div>
)

}
