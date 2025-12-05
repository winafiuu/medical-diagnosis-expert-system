import { useMutation } from '@tanstack/react-query'
import {
  startDiagnosis,
  submitAnswer,
  type DiagnoseResponse,
} from '../api/diagnosis'
import { useDiagnosisStore } from '../store/diagnosisStore'

export const useStartDiagnosis = () => {
  const {
    setSessionId,
    setLoading,
    setError,
    resetDiagnosis,
    setCurrentQuestion,
    setCurrentSymptomId,
    addMessage,
  } = useDiagnosisStore()

  return useMutation({
    mutationFn: startDiagnosis,
    onMutate: () => {
      resetDiagnosis()
      setLoading(true)
      setError(null)
    },
    onSuccess: (response: DiagnoseResponse) => {
      setLoading(false)
      if (response.success && response.sessionId) {
        setSessionId(response.sessionId)

        // Handle initial question
        const nextQuestion = response.data.next_question
        if (nextQuestion) {
          setCurrentQuestion(nextQuestion.text)
          setCurrentSymptomId(nextQuestion.symptom)
          // Add system message
          addMessage({
            id: crypto.randomUUID(),
            sender: 'system',
            content: nextQuestion.text,
            timestamp: Date.now(),
          })
        }
      } else {
        setError(response.message || 'Failed to start diagnosis')
      }
    },
    onError: (error: any) => {
      setLoading(false)
      setError(error.message || 'An error occurred')
    },
  })
}

export const useSubmitAnswer = () => {
  const {
    sessionId,
    currentSymptomId,
    setLoading,
    setError,
    setCurrentQuestion,
    setCurrentSymptomId,
    setDiagnosisResult,
    addMessage,
  } = useDiagnosisStore()

  return useMutation({
    mutationFn: ({
      certainty,
      symptomOverride, // Optional: allow component to pass symptom explicitly if needed, otherwise use store
    }: {
      certainty: number
      symptomOverride?: string
    }) => {
      if (!sessionId) throw new Error('No active session')
      // Use the override if provided, otherwise the stored symptom ID
      const symptomToSubmit = symptomOverride || currentSymptomId

      if (!symptomToSubmit) throw new Error('No current symptom to answer for')

      return submitAnswer(sessionId, symptomToSubmit, certainty)
    },
    onMutate: () => {
      setLoading(true)
      setError(null)
    },
    onSuccess: (response: DiagnoseResponse) => {
      setLoading(false)
      if (response.success) {
        const { next_question, diagnosis } = response.data

        if (next_question) {
          setCurrentQuestion(next_question.text)
          setCurrentSymptomId(next_question.symptom)
          addMessage({
            id: crypto.randomUUID(),
            sender: 'system',
            content: next_question.text,
            timestamp: Date.now(),
          })
        } else if (diagnosis) {
          setCurrentQuestion(null)
          setCurrentSymptomId(null)

          // Map backend response (disease, certainty) to store (disease, confidence)
          const mappedDiagnosis = Array.isArray(diagnosis)
            ? diagnosis.map((d: any) => ({
                disease: d.disease,
                confidence: d.certainty,
                explanation: d.explanation, // assuming backend might send this later
                description: d.description,
              }))
            : []

          setDiagnosisResult(mappedDiagnosis)
          addMessage({
            id: crypto.randomUUID(),
            sender: 'system',
            content: 'Diagnosis complete. See results below.',
            timestamp: Date.now(),
          })
        }
      } else {
        setError(response.message || 'Failed to submit answer')
      }
    },
    onError: (error: any) => {
      setLoading(false)
      setError(error.message || 'An error occurred')
    },
  })
}
