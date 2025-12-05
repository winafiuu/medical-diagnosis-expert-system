import { DiagnosisCard } from '@/components/DiagnosisCard'
import { useNavigate } from 'react-router-dom'

export default function Result() {
  const navigate = useNavigate()

  // Mock result for layout demonstration
  const mockResult = {
    disease: 'Influenza (Flu)',
    description: 'A viral infection that attacks your respiratory system.',
    confidence: 0.85,
    explanation:
      'High confidence match due to presence of fever (CF 0.9), fatigue (CF 0.8), and body aches. The absence of breathing difficulty lowers the probability of Pneumonia.',
  }

  const handleRestart = () => {
    navigate('/diagnosis')
  }

  return (
    <div className="flex flex-col items-center w-full py-8">
      <DiagnosisCard result={mockResult} onRestart={handleRestart} />
    </div>
  )
}
