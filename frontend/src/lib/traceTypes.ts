export interface TraceFlags {
  is_slow_step: boolean
  is_expensive_step: boolean
}

export interface TraceNode {
  id: string
  type: string
  error: string | null
  tokens: number
  latency: number
  parent_id: string | null
  children: TraceNode[]
  flags: TraceFlags
}
