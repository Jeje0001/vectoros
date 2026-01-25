export default function RunsLayout({ children }: { children: React.ReactNode }) {
  return (
    <div className="flex h-screen">
      

      <main className="flex-1 p-4">
        {children}
      </main>
    </div>
  );
}
