import { useEffect, useState, useRef } from 'react'
import { useNavigate } from 'react-router-dom'
import { ChatContainer } from '@/components/ChatContainer'
import { QuickResponseButtons } from '@/components/QuickResponseButtons'
import { SymptomSlider } from '@/components/SymptomSlider'
import { Button } from '@/components/ui/button'
import { useDiagnosisStore } from '@/store/diagnosisStore'
import { useStartDiagnosis, useSubmitAnswer } from '@/hooks/useDiagnosis'

export default function Diagnosis() {
  const navigate = useNavigate()
  const {
    messages,
    currentQuestion,
    diagnosisResult,
    error,
    addMessage,
    sessionId,
    isLoading,
  } = useDiagnosisStore()
  const { mutate: startDiagnosis } = useStartDiagnosis()
  const { mutate: submitAnswer } = useSubmitAnswer()

  const hasStartedRef = useRef(false)

  const [sliderValue, setSliderValue] = useState(50)

  // Start diagnosis on mount
  useEffect(() => {
    if (hasStartedRef.current || sessionId) return
    hasStartedRef.current = true
    startDiagnosis()
  }, [sessionId, startDiagnosis])

  // Redirect to result if diagnosis is complete
  useEffect(() => {
    if (diagnosisResult) {
      navigate('/result')
    }
  }, [diagnosisResult, navigate])

  const addUserMessage = (text: string) => {
    addMessage({
      id: crypto.randomUUID(),
      sender: 'user',
      content: text,
      timestamp: Date.now(),
    })
  }

  const handleQuickResponse = (type: string, cf?: number) => {
    let certainty = 0.5
    let text = 'Unsure'

    // cf from QuickResponseButtons is 0-100 scales
    if (cf !== undefined) {
      certainty = cf / 100

      // Format display text nicely
      if (type === 'yes') text = 'Yes'
      else if (type === 'no') text = 'No'
      else if (type === 'unsure') text = 'Unsure'
      else text = `${type} (${cf}%)`
    } else {
      // Fallback if no CF provided (shouldn't happen with updated buttons but safe to keep)
      if (type === 'yes') {
        certainty = 1.0
        text = 'Yes'
      }
      if (type === 'no') {
        certainty = 0.0
        text = 'No'
      }
      if (type === 'unsure') {
        certainty = 0.5
        text = 'Unsure'
      }
    }

    addUserMessage(text)
    submitAnswer({ certainty })
  }

  const handleSliderSubmit = () => {
    addUserMessage(`Certainty: ${sliderValue}%`)
    submitAnswer({ certainty: sliderValue / 100 })
  }

  // Use the global store loading state which is explicitly managed by our hooks
  const isBusy = isLoading

  return (
    <div className="flex flex-col h-[calc(100vh-140px)] w-full max-w-4xl mx-auto">
      <div className="text-center space-y-2 mb-4 shrink-0">
        <h2 className="text-2xl font-bold tracking-tight text-foreground">
          Diagnosis Session
        </h2>
        <p className="text-muted-foreground text-sm">
          Answer truthfully for accurate results.
        </p>
      </div>

      <div className="flex-1 min-h-0 mb-4 overflow-hidden border border-border/50 rounded-2xl bg-muted/30 backdrop-blur-sm shadow-inner">
        <ChatContainer
          messages={messages}
          isLoading={isBusy && !currentQuestion}
        />
      </div>

      {error && (
        <div className="p-3 mb-4 text-sm text-destructive bg-destructive/10 rounded-lg border border-destructive/20">
          Error: {error}
        </div>
      )}

      {/* Input Area */}
      <div className="shrink-0 space-y-4 p-4 bg-card/50 backdrop-blur-md rounded-2xl border border-border shadow-sm">
        {currentQuestion ? (
          <div className="space-y-4 animate-in fade-in slide-in-from-bottom-4 duration-500">
            <p className="text-sm font-medium text-center text-foreground/80">
              {currentQuestion}
            </p>

            <QuickResponseButtons
              onSelect={handleQuickResponse}
              disabled={isBusy}
            />

            <div className="flex items-end gap-4">
              <div className="flex-1">
                <SymptomSlider value={sliderValue} onChange={setSliderValue} />
              </div>
              <Button
                onClick={handleSliderSubmit}
                disabled={isBusy}
                className="mb-1 h-10 px-6"
              >
                Submit
              </Button>
            </div>
          </div>
        ) : (
          <div className="text-center text-muted-foreground py-8">
            {isBusy
              ? 'Consulting the expert system...'
              : 'Session Initialization...'}
          </div>
        )}
      </div>
    </div>
  )
}
