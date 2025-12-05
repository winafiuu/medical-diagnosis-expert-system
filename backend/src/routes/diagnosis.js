import express from 'express'
import {
  startDiagnosis,
  submitAnswer,
  getDiagnosis,
  endDiagnosis,
} from '../controllers/diagnosisController.js'

const router = express.Router()

// POST /api/diagnose/start - Initialize a new diagnosis session
router.post('/start', startDiagnosis)

// POST /api/diagnose/answer - Submit an answer and get next question or result
router.post('/answer', submitAnswer)

// POST /api/diagnose/result - Get final diagnosis
router.post('/result', getDiagnosis)

// POST /api/diagnose/end - Terminate a session
router.post('/end', endDiagnosis)

export default router
