import "./globals.css"
import Sidebar from "@/components/ui/Sidebar"
import { Inter, JetBrains_Mono } from "next/font/google"

const inter = Inter({
  subsets: ["latin"],
  variable: "--font-sans"
})

const jetbrains = JetBrains_Mono({
  subsets: ["latin"],
  variable: "--font-mono"
})

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
<html
  lang="en"
  className={`dark ${inter.variable} ${jetbrains.variable}`}
>
      <body className="min-h-screen bg-background text-foreground antialiased">
        <div className="h-screen flex">
          <aside className="w-72 border-r border-border bg-sidebar">
            <div className="h-full p-3">
              <Sidebar />
            </div>
          </aside>

          <main className="flex-1 overflow-hidden">
            {children}
          </main>
        </div>
      </body>
    </html>
  )
}
