import express from 'express'
import {
  startDiagnosis,
  submitAnswer,
} from '../controllers/diagnosisController.js'

const router = express.Router()

// POST /api/diagnose/start - Initialize a new diagnosis session
router.post('/start', startDiagnosis)

// POST /api/diagnose/answer - Submit an answer and get next question or result
router.post('/answer', submitAnswer)

export default router
