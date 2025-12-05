import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { ChatContainer } from '@/components/ChatContainer'
import { ChatInput } from '@/components/ChatInput'
import { QuickResponseButtons } from '@/components/QuickResponseButtons'
import { SymptomSlider } from '@/components/SymptomSlider'
import { Button } from '@/components/ui/button'
import { useDiagnosisStore } from '@/store/diagnosisStore'
import { useStartDiagnosis, useSubmitAnswer } from '@/hooks/useDiagnosis'

export default function Diagnosis() {
  const navigate = useNavigate()
  const { messages, isLoading, currentQuestion, diagnosisResult, error } =
    useDiagnosisStore()
  const { mutate: startDiagnosis, isPending: isStarting } = useStartDiagnosis()
  const { mutate: submitAnswer, isPending: isSubmitting } = useSubmitAnswer()

  const [sliderValue, setSliderValue] = useState(50)

  // Start diagnosis on mount
  useEffect(() => {
    // Only start if we don't have messages or specific state
    // Actually, always start fresh for "Diagnosis" page is usually expected,
    // or we could check if session exists.
    // For now, let's start fresh.
    startDiagnosis()
  }, []) // eslint-disable-line react-hooks/exhaustive-deps

  // Redirect to result if diagnosis is complete
  useEffect(() => {
    if (diagnosisResult) {
      navigate('/result')
    }
  }, [diagnosisResult, navigate])

  const handleQuickResponse = (type: string, cf?: number) => {
    let certainty = 0.5
    // cf from QuickResponseButtons is 0-100
    if (cf !== undefined) {
      certainty = cf / 100
    } else {
      // Fallback defaults
      if (type === 'yes') certainty = 1.0
      if (type === 'no') certainty = 0.0
      if (type === 'unsure') certainty = 0.5
    }

    submitAnswer({ certainty })
  }

  const handleSliderSubmit = () => {
    submitAnswer({ certainty: sliderValue / 100 })
  }

  const handleTextSubmit = (text: string) => {
    const lower = text.toLowerCase()
    if (lower.match(/\b(yes|yeah|sure|yep|definitely)\b/)) {
      submitAnswer({ certainty: 1.0 })
    } else if (lower.match(/\b(no|nope|nah|none|not)\b/)) {
      submitAnswer({ certainty: 0.0 })
    } else if (lower.match(/\b(maybe|unsure|dont know|dunno)\b/)) {
      submitAnswer({ certainty: 0.5 })
    } else {
      // Simple heuristic failed
      // using alert or console for now if no toast
      console.log('Could not parse response:', text)
    }
  }

  const isBusy = isLoading || isStarting || isSubmitting

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

            <div className="relative py-2">
              <div className="absolute inset-0 flex items-center">
                <span className="w-full border-t" />
              </div>
              <div className="relative flex justify-center text-xs uppercase">
                <span className="bg-background px-2 text-muted-foreground">
                  Or be precise
                </span>
              </div>
            </div>

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

            <div className="pt-2">
              <ChatInput
                onSend={handleTextSubmit}
                disabled={isBusy}
                placeholder="Type 'yes', 'no', or 'unsure'..."
              />
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
