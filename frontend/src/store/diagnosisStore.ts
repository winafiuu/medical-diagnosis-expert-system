import { create } from 'zustand'

export type MessageRole = 'user' | 'system'

export interface ChatMessage {
  id: string
  sender: MessageRole
  content: string
  timestamp: number
}

export interface DiagnosisResult {
  disease: string
  confidence: number
  description?: string
  explanation?: string
  recommendations?: string[]
}

export interface DiagnosisState {
  sessionId: string | null
  messages: ChatMessage[]
  currentQuestion: string | null
  currentSymptomId: string | null
  diagnosisResult: DiagnosisResult[] | null
  isLoading: boolean
  error: string | null

  // Actions
  setSessionId: (sessionId: string | null) => void
  addMessage: (message: ChatMessage) => void
  setCurrentQuestion: (question: string | null) => void
  setCurrentSymptomId: (symptomId: string | null) => void
  setDiagnosisResult: (result: DiagnosisResult[] | null) => void
  setLoading: (isLoading: boolean) => void
  setError: (error: string | null) => void
  resetDiagnosis: () => void
}

export const useDiagnosisStore = create<DiagnosisState>((set) => ({
  sessionId: null,
  messages: [],
  currentQuestion: null,
  currentSymptomId: null,
  diagnosisResult: null,
  isLoading: false,
  error: null,

  setSessionId: (sessionId) => set({ sessionId }),
  addMessage: (message) =>
    set((state) => ({ messages: [...state.messages, message] })),
  setCurrentQuestion: (question) => set({ currentQuestion: question }),
  setCurrentSymptomId: (symptomId) => set({ currentSymptomId: symptomId }),
  setDiagnosisResult: (result) => set({ diagnosisResult: result }),
  setLoading: (isLoading) => set({ isLoading }),
  setError: (error) => set({ error }),
  resetDiagnosis: () =>
    set({
      sessionId: null,
      messages: [],
      currentQuestion: null,
      currentSymptomId: null,
      diagnosisResult: null,
      isLoading: false,
      error: null,
    }),
}))
