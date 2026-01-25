export default function RunLoading() {
  return (
    <div className="p-6 space-y-4">
      <div className="h-6 w-1/4 bg-muted rounded animate-pulse" />

      <div className="h-24 bg-muted rounded animate-pulse" />

      <div className="grid grid-cols-3 gap-4">
        <div className="h-6 bg-muted rounded animate-pulse" />
        <div className="h-6 bg-muted rounded animate-pulse" />
        <div className="h-6 bg-muted rounded animate-pulse" />
      </div>

      <div className="h-16 bg-muted rounded animate-pulse" />

      <div className="h-40 bg-muted rounded animate-pulse" />
    </div>
  )
}
