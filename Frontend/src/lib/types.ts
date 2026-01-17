export interface Run {
  run_id: string
  model: string
  input: string
  output: string
  tokens: number
  cost: number
  latency: number
  status: string
  error: string | null
}

export interface StepFlags {
  is_slow_step: boolean
  is_expensive_step: boolean
}



export interface Step {
  id: string
  children: Step[]
  flags: StepFlags

  [key: string]: unknown
}

export interface RunSummary {
  run_id: string
  status: string
  created_at: string | null
  input: string | null
}
