import sessionManager from '../services/sessionManager.js'

/**
 * Start a new diagnosis session
 * POST /api/diagnose/start
 */
export const startDiagnosis = async (req, res) => {
  try {
    const { sessionId, result } = await sessionManager.createSession()

    res.json({
      success: true,
      sessionId,
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
 * Body: { sessionId: string, symptom: string, certainty: number (0-1) }
 */
export const submitAnswer = async (req, res) => {
  try {
    const { sessionId, symptom, certainty } = req.body

    // Validate input
    if (!sessionId) {
      return res.status(400).json({
        success: false,
        error: 'Invalid request',
        message: 'sessionId is required',
      })
    }

    if (!symptom) {
      return res.status(400).json({
        success: false,
        error: 'Invalid request',
        message: 'symptom is required',
      })
    }

    if (certainty === undefined || certainty < 0 || certainty > 1) {
      return res.status(400).json({
        success: false,
        error: 'Invalid request',
        message: 'certainty must be between 0 and 1',
      })
    }

    const result = await sessionManager.sendCommand(sessionId, {
      action: 'add_symptom',
      symptom,
      certainty,
    })

    res.json({
      success: true,
      data: result,
    })
  } catch (error) {
    console.error('Error processing answer:', error)

    if (error.message === 'Session not found') {
      return res.status(404).json({
        success: false,
        error: 'Session not found',
        message: 'The session may have expired. Please start a new diagnosis.',
      })
    }

    res.status(500).json({
      success: false,
      error: 'Failed to process answer',
      message: error.message,
    })
  }
}

/**
 * Get final diagnosis for a session
 * POST /api/diagnose/result
 * Body: { sessionId: string }
 */
export const getDiagnosis = async (req, res) => {
  try {
    const { sessionId } = req.body

    if (!sessionId) {
      return res.status(400).json({
        success: false,
        error: 'Invalid request',
        message: 'sessionId is required',
      })
    }

    const result = await sessionManager.sendCommand(sessionId, {
      action: 'get_diagnosis',
    })

    res.json({
      success: true,
      data: result,
    })
  } catch (error) {
    console.error('Error getting diagnosis:', error)

    if (error.message === 'Session not found') {
      return res.status(404).json({
        success: false,
        error: 'Session not found',
        message: 'The session may have expired. Please start a new diagnosis.',
      })
    }

    res.status(500).json({
      success: false,
      error: 'Failed to get diagnosis',
      message: error.message,
    })
  }
}

/**
 * Terminate a diagnosis session
 * POST /api/diagnose/end
 * Body: { sessionId: string }
 */
export const endDiagnosis = async (req, res) => {
  try {
    const { sessionId } = req.body

    if (!sessionId) {
      return res.status(400).json({
        success: false,
        error: 'Invalid request',
        message: 'sessionId is required',
      })
    }

    sessionManager.terminateSession(sessionId)

    res.json({
      success: true,
      message: 'Session terminated successfully',
    })
  } catch (error) {
    console.error('Error ending diagnosis:', error)
    res.status(500).json({
      success: false,
      error: 'Failed to end session',
      message: error.message,
    })
  }
}
