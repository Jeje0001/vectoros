"use client";

import { useEffect, useState } from "react";
import { getInputPreview, getAnchorId, getRelativeTime } from "@/lib/sidebarFormat"
import { useRouter } from "next/navigation"
import { usePathname } from "next/navigation"


interface RunSummary {
  run_id: string
  model: string
  status: string
  created_at: string
  input: string | null
}

function getActiveRunIdFromPath(pathname: string): string | null {
  const prefix = "/runs/"

  if (pathname.startsWith(prefix) === false) {
    return null
  }

  const parts = pathname.split(prefix)
  if (parts.length < 2) {
    return null
  }

  const idPart = parts[1]
  if (idPart.length === 0) {
    return null
  }

  return idPart
}


export default function Sidebar() {
  const router = useRouter()
  const pathname = usePathname()
  const activeRunId = getActiveRunIdFromPath(pathname)



  const [runs, setRuns] = useState<RunSummary[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function loadRuns() {
      try {
        const response = await fetch(
          `${process.env.NEXT_PUBLIC_API_URL}/runs`
        );

        if (!response.ok) {
          throw new Error("Failed to fetch runs");
        }

        const data = await response.json();
        setRuns(data.items);
      } catch (err) {
        setError("Error loading runs");
      } finally {
        setLoading(false);
      }
    }

    loadRuns();
  }, []);

  if (loading) {
    return <div className="p-3 text-sm">Loading runs...</div>;
  }

  if (error) {
    return <div className="p-3 text-sm text-red-500">{error}</div>;
  }

  return (
    <div className="p-3 space-y-2">
      <div className="text-sm font-semibold mb-2">Run History</div>

      {runs.length === 0 && (
        <div className="text-xs text-muted-foreground">
          No runs yet
        </div>
      )}

      {runs.map((run) => {
          const isActive = activeRunId !== null && run.run_id === activeRunId

          const preview = getInputPreview(run.input)
          const anchor = getAnchorId(run.run_id)
          const time = getRelativeTime(run.created_at)
          let cardClassName =
          "relative border rounded p-2 text-xs cursor-pointer space-y-1 transition-colors"

          if (isActive === true) {
            cardClassName += " border-primary bg-muted"
          } else {
            cardClassName += " hover:bg-muted"
        }


          return (
            <div
              key={run.run_id}
              className={cardClassName}
              onClick={() => {
                router.push(`/runs/${run.run_id}`)
              }}
            >
              {isActive === true && (
                <div className="absolute left-0 top-0 h-full w-1 bg-primary rounded-l" />
              )}

              <div className="font-medium truncate">
                {preview}
              </div>

              <div className="text-muted-foreground flex justify-between">
                <span>{time} • {run.model}</span>
                <span>{anchor}</span>
              </div>

              <div className="text-xs">
                {run.status === "success" && (
                  <span className="text-green-500">✓ Success</span>
                )}
                {run.status === "failure" && (
                  <span className="text-red-500">✕ Failure</span>
                )}
                {run.status === "pending" && (
                  <span className="text-yellow-500">• Pending</span>
                )}
              </div>
            </div>
          )

        })}

    </div>
  );
}
