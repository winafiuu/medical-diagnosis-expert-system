import { ArrowRight, ShieldCheck, Zap, Brain } from 'lucide-react'
import { Link } from 'react-router-dom'

export default function Home() {
  return (
    <div className="flex flex-col items-center justify-center min-h-[80vh] text-center space-y-12">
      <div className="space-y-6 max-w-3xl">
        <div className="inline-flex items-center rounded-full border border-blue-200 bg-blue-50 px-3 py-1 text-sm font-medium text-blue-800">
          <span className="flex h-2 w-2 rounded-full bg-blue-600 mr-2"></span>
          AI-Powered Medical Diagnosis
        </div>

        <h1 className="text-4xl font-extrabold tracking-tight sm:text-6xl text-slate-900">
          Smart Health Insights <br className="hidden sm:inline" />
          <span className="text-blue-600">Powered by Expert Systems</span>
        </h1>

        <p className="text-xl text-slate-600 max-w-2xl mx-auto leading-relaxed">
          Get preliminary diagnostic insights for respiratory illnesses using
          our advanced expert system rules and fuzzy logic engine.
        </p>

        <div className="flex flex-col sm:flex-row gap-4 justify-center pt-4">
          <Link
            to="/diagnosis"
            className="inline-flex items-center justify-center h-12 px-8 rounded-lg bg-blue-600 text-white font-medium hover:bg-blue-700 transition-colors shadow-lg hover:shadow-xl shadow-blue-200"
          >
            Start Diagnosis
            <ArrowRight className="ml-2 h-5 w-5" />
          </Link>
          <a
            href="https://github.com/winafiuu/medical-diagnosis-expert-system"
            target="_blank"
            rel="noreferrer"
            className="inline-flex items-center justify-center h-12 px-8 rounded-lg border border-slate-200 bg-white text-slate-700 font-medium hover:bg-slate-50 transition-colors"
          >
            View on GitHub
          </a>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-8 w-full max-w-5xl pt-12">
        <FeatureCard
          icon={<Brain className="h-8 w-8 text-blue-500" />}
          title="Rule-Based Engine"
          description="Powered by the Experta Python library, utilizing forward and backward chaining for accurate logical deductions."
        />
        <FeatureCard
          icon={<Zap className="h-8 w-8 text-amber-500" />}
          title="Certainty Factors"
          description="Handles uncertainty and fuzzy data, providing diagnosis confidence scores for more realistic assessments."
        />
        <FeatureCard
          icon={<ShieldCheck className="h-8 w-8 text-green-500" />}
          title="Medical Guidelines"
          description="Rules derived from standard medical guidelines for respiratory conditions like Flu, COVID-19, and Pneumonia."
        />
      </div>
    </div>
  )
}

function FeatureCard({
  icon,
  title,
  description,
}: {
  icon: React.ReactNode
  title: string
  description: string
}) {
  return (
    <div className="bg-white p-6 rounded-2xl shadow-sm border border-slate-100 hover:shadow-md transition-shadow text-left">
      <div className="mb-4 bg-slate-50 w-14 h-14 rounded-xl flex items-center justify-center">
        {icon}
      </div>
      <h3 className="text-lg font-bold text-slate-900 mb-2">{title}</h3>
      <p className="text-slate-600 leading-relaxed">{description}</p>
    </div>
  )
}
