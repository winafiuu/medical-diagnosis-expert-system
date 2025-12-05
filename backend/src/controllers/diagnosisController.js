import { runDiagnosisEngine } from '../services/pythonService.js'

/**
 * Start a new diagnosis session
 * POST /api/diagnose/start
 */
export const startDiagnosis = async (req, res) => {
  try {
    const result = await runDiagnosisEngine({ action: 'start' })

    res.json({
      success: true,
      data: result,
    })
  } catch (error) {
    console.error('Error starting diagnosis:', error)
    res.status(500).json({
      success: false,
      error: 'Failed to start diagnosis session',
      message: error.message,
    })
  }
}

/**
 * Submit an answer and get next question or final diagnosis
 * POST /api/diagnose/answer
 * Body: { symptom: string, certainty: number (0-100), answers: object }
 */
export const submitAnswer = async (req, res) => {
  try {
    const { symptom, certainty, answers } = req.body

    // Validate input
    if (!answers || typeof answers !== 'object') {
      return res.status(400).json({
        success: false,
        error: 'Invalid request',
        message: 'answers object is required',
      })
    }

    const result = await runDiagnosisEngine({
      action: 'answer',
      symptom,
      certainty,
      answers,
    })

    res.json({
      success: true,
      data: result,
    })
  } catch (error) {
    console.error('Error processing answer:', error)
    res.status(500).json({
      success: false,
      error: 'Failed to process answer',
      message: error.message,
    })
  }
}
