export default function RunsLayout({ children }: { children: React.ReactNode }) {
  return (
    <div className="flex h-screen">
      <aside className="w-64 border-r p-4">
        {/* Sidebar placeholder */}
        <div>Sidebar</div>
      </aside>

      <main className="flex-1 p-4">
        {children}
      </main>
    </div>
  );
}
