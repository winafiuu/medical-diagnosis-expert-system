import { create } from 'zustand'

export interface ChatMessage {
  id: string
  sender: 'user' | 'system'
  content: string
  timestamp: number
}

export interface DiagnosisResult {
  diagnosis: string
  confidence: number
  explanation?: string
  recommendations?: string[]
}

interface DiagnosisState {
  sessionId: string | null
  messages: ChatMessage[]
  currentQuestion: string | null
  diagnosisResult: DiagnosisResult[] | null
  isLoading: boolean
  error: string | null

  // Actions
  setSessionId: (sessionId: string | null) => void
  addMessage: (message: ChatMessage) => void
  setCurrentQuestion: (question: string | null) => void
  setDiagnosisResult: (result: DiagnosisResult[] | null) => void
  setLoading: (isLoading: boolean) => void
  setError: (error: string | null) => void
  resetDiagnosis: () => void
}

export const useDiagnosisStore = create<DiagnosisState>((set) => ({
  sessionId: null,
  messages: [],
  currentQuestion: null,
  diagnosisResult: null,
  isLoading: false,
  error: null,

  setSessionId: (sessionId) => set({ sessionId }),
  addMessage: (message) =>
    set((state) => ({ messages: [...state.messages, message] })),
  setCurrentQuestion: (question) => set({ currentQuestion: question }),
  setDiagnosisResult: (result) => set({ diagnosisResult: result }),
  setLoading: (isLoading) => set({ isLoading }),
  setError: (error) => set({ error }),
  resetDiagnosis: () =>
    set({
      sessionId: null,
      messages: [],
      currentQuestion: null,
      diagnosisResult: null,
      isLoading: false,
      error: null,
    }),
}))
