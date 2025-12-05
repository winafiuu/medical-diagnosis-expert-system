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
    setLoading,
    setError,
    setCurrentQuestion,
    setDiagnosisResult,
    addMessage,
  } = useDiagnosisStore()

  return useMutation({
    mutationFn: ({
      symptom,
      certainty,
    }: {
      symptom: string
      certainty: number
    }) => {
      if (!sessionId) throw new Error('No active session')
      return submitAnswer(sessionId, symptom, certainty)
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
          addMessage({
            id: crypto.randomUUID(),
            sender: 'system',
            content: next_question.text,
            timestamp: Date.now(),
          })
        } else if (diagnosis) {
          setCurrentQuestion(null)
          setDiagnosisResult(diagnosis)
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
