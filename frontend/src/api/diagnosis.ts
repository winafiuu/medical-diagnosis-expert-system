import api from './axios'

export interface DiagnoseResponse {
  success: boolean
  sessionId?: string
  data: any // Ideally we should define the shape of the data from the expert system
  error?: string
  message?: string
}

export const startDiagnosis = async (): Promise<DiagnoseResponse> => {
  const response = await api.post<DiagnoseResponse>('/diagnose/start')
  return response.data
}

export const submitAnswer = async (
  sessionId: string,
  symptom: string,
  certainty: number
): Promise<DiagnoseResponse> => {
  const response = await api.post<DiagnoseResponse>('/diagnose/answer', {
    sessionId,
    symptom,
    certainty,
  })
  return response.data
}

export const getDiagnosis = async (
  sessionId: string
): Promise<DiagnoseResponse> => {
  const response = await api.post<DiagnoseResponse>('/diagnose/result', {
    sessionId,
  })
  return response.data
}

export const endDiagnosis = async (
  sessionId: string
): Promise<DiagnoseResponse> => {
  const response = await api.post<DiagnoseResponse>('/diagnose/end', {
    sessionId,
  })
  return response.data
}
