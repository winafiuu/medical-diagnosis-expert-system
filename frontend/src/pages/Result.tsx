import { useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { DiagnosisCard } from '@/components/DiagnosisCard'
import { useDiagnosisStore } from '@/store/diagnosisStore'

export default function Result() {
  const navigate = useNavigate()
  const { diagnosisResult, resetDiagnosis } = useDiagnosisStore()

  useEffect(() => {
    // If no result, redirect to home
    if (!diagnosisResult || diagnosisResult.length === 0) {
      // Small delay to allow store to update if it was just mounted (though unlikely if navigated here)
      // But typically we should redirect if accessed directly without result
      const t = setTimeout(() => {
        if (!useDiagnosisStore.getState().diagnosisResult) {
          navigate('/')
        }
      }, 500)
      return () => clearTimeout(t)
    }
  }, [diagnosisResult, navigate])

  const handleRestart = () => {
    resetDiagnosis()
    navigate('/diagnosis')
  }

  if (!diagnosisResult || diagnosisResult.length === 0) {
    return (
      <div className="p-8 text-center text-muted-foreground">
        Loading results...
      </div>
    )
  }

  // Sort by confidence descending and pick top result
  const sortedResults = [...diagnosisResult].sort(
    (a, b) => b.confidence - a.confidence
  )
  const topResult = sortedResults[0]

  return (
    <div className="flex flex-col items-center w-full py-8 px-4">
      <DiagnosisCard result={topResult} onRestart={handleRestart} />

      {/* Optional: Show secondary results if any */}
      {sortedResults.length > 1 && (
        <div className="mt-8 w-full max-w-2xl">
          <h3 className="text-md font-semibold text-muted-foreground mb-2">
            Other Possibilities
          </h3>
          <div className="space-y-2">
            {sortedResults.slice(1).map((res, idx) => (
              <div
                key={idx}
                className="flex justify-between p-3 bg-muted/20 rounded-lg text-sm"
              >
                <span>{res.disease}</span>
                <span className="font-mono text-muted-foreground">
                  {Math.round(res.confidence * 100)}%
                </span>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}
