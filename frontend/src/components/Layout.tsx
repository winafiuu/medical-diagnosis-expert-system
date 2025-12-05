import React from 'react'
import { Link, Outlet } from 'react-router-dom'
import { Activity } from 'lucide-react'

const Layout: React.FC = () => {
  return (
    <div className="min-h-screen bg-slate-50 flex flex-col font-sans text-slate-900">
      {/* Header */}
      <header className="sticky top-0 z-50 w-full border-b border-slate-200 bg-white/75 backdrop-blur supports-backdrop-filter:bg-white/60">
        <div className="container mx-auto px-4 h-16 flex items-center justify-between">
          <Link
            to="/"
            className="flex items-center gap-2 hover:opacity-80 transition-opacity"
          >
            <div className="bg-blue-600 p-1.5 rounded-lg text-white">
              <Activity className="h-6 w-6" />
            </div>
            <span className="font-bold text-xl tracking-tight text-slate-900">
              Medi<span className="text-blue-600">Diagnose</span>
            </span>
          </Link>

          <nav className="flex items-center gap-6 text-sm font-medium text-slate-600">
            <Link to="/" className="hover:text-blue-600 transition-colors">
              Home
            </Link>
            <Link
              to="/diagnosis"
              className="hover:text-blue-600 transition-colors"
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
      <footer className="border-t border-slate-200 py-6 bg-white">
        <div className="container mx-auto px-4 text-center text-sm text-slate-500">
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
