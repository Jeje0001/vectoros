import RunDetailClient from "@/components/ui/trace/RunDetailClient"

export default async function RunDetailPage({
  params
}: {
  params: Promise<{ id: string }>
}) {
  const { id } = await params

  const res = await fetch(
    `${process.env.NEXT_PUBLIC_API_URL}/runs/${id}`,
    { cache: "no-store" }
  )

  if (!res.ok) {
    const error = await res.json()
    return (
      <div className="p-6 space-y-2">
        <h2 className="text-lg font-semibold text-red-500">Unable to load run</h2>
        <p className="text-sm text-muted-foreground">
          {error.detail ?? "This run cannot be displayed."}
        </p>
      </div>
    )
  }

  const data = await res.json()
  const run = data.run
  const tree = data.tree

  return <RunDetailClient run={run} tree={tree} />
}
