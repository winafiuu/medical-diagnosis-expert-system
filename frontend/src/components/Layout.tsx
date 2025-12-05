import React from 'react'
import { Link, Outlet } from 'react-router-dom'
import { Activity } from 'lucide-react'

const Layout: React.FC = () => {
  return (
    <div className="min-h-screen bg-background flex flex-col font-sans text-foreground selection:bg-primary/20">
      {/* Header */}
      <header className="sticky top-0 z-50 w-full border-b border-border/40 bg-background/80 backdrop-blur-md supports-backdrop-filter:bg-background/60">
        <div className="container mx-auto px-4 h-16 flex items-center justify-between">
          <Link
            to="/"
            className="flex items-center gap-2 hover:opacity-80 transition-opacity"
          >
            <div className="bg-primary/10 p-2 rounded-xl text-primary ring-1 ring-primary/20">
              <Activity className="h-6 w-6" />
            </div>
            <span className="font-bold text-xl tracking-tight text-foreground">
              Medi<span className="text-primary">Diagnose</span>
            </span>
          </Link>

          <nav className="flex items-center gap-6 text-sm font-medium text-muted-foreground">
            <Link to="/" className="hover:text-primary transition-colors">
              Home
            </Link>
            <Link
              to="/diagnosis"
              className="hover:text-primary transition-colors"
            >
              New Diagnosis
            </Link>
          </nav>
        </div>
      </header>

      {/* Main Content */}
      <main className="flex-1 container mx-auto px-4 py-8 max-w-5xl">
        <Outlet />
      </main>

      {/* Footer */}
      <footer className="border-t border-border/40 py-6 bg-background/50 backdrop-blur-sm">
        <div className="container mx-auto px-4 text-center text-sm text-muted-foreground">
          <p>
            &copy; {new Date().getFullYear()} MediDiagnose Expert System. For
            educational purposes only.
          </p>
        </div>
      </footer>
    </div>
  )
}

export default Layout
