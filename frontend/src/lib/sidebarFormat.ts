export function getInputPreview(input: string | null, max = 30): string {
  if (!input) return "No input provided";
  const singleLine = input.replace(/\s+/g, " ").trim();
  if (singleLine.length <= max) return singleLine;
  return singleLine.slice(0, max) + "…";
}

export function getAnchorId(runId: string): string {
  return "…" + runId.slice(-4);
}

export function getRelativeTime(iso: string): string {
  const now = Date.now();
  const then = new Date(iso).getTime();
  const diff = Math.floor((now - then) / 1000);

  if (diff < 60) return "just now";
  if (diff < 3600) return `${Math.floor(diff / 60)}m ago`;
  if (diff < 86400) return `${Math.floor(diff / 3600)}h ago`;
  return `${Math.floor(diff / 86400)}d ago`;
}
