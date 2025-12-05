# Backend API Testing Guide

This document provides examples of how to test the Medical Diagnosis API endpoints.

## Base URL

```
http://localhost:3000
```

## Endpoints

### 1. Start Diagnosis Session

**POST** `/api/diagnose/start`

Initializes a new diagnosis session and returns the first question.

**Request:**

```bash
curl -X POST http://localhost:3000/api/diagnose/start \
  -H "Content-Type: application/json"
```

**Response:**

```json
{
  "success": true,
  "sessionId": "a8f1dabc-9bac-4e2a-a12f-fd6447aaf5c7",
  "data": {
    "status": "success",
    "message": "Diagnosis session started",
    "next_question": {
      "symptom": "fever",
      "text": "Do you have a fever (elevated body temperature)?"
    }
  }
}
```

### 2. Submit Answer

**POST** `/api/diagnose/answer`

Submits an answer to a symptom question and receives the next question or final diagnosis.

**Request Body:**

- `sessionId` (string, required): The session ID from the start endpoint
- `symptom` (string, required): The symptom name from the question
- `certainty` (number, required): Certainty level between 0 and 1 (0 = no, 1 = yes)

**Request:**

```bash
curl -X POST http://localhost:3000/api/diagnose/answer \
  -H "Content-Type: application/json" \
  -d '{
    "sessionId": "a8f1dabc-9bac-4e2a-a12f-fd6447aaf5c7",
    "symptom": "fever",
    "certainty": 0.9
  }'
```

**Response (Next Question):**

```json
{
  "success": true,
  "data": {
    "status": "success",
    "message": "Symptom recorded",
    "next_question": {
      "symptom": "loss_of_smell",
      "text": "Have you lost your sense of smell?"
    }
  }
}
```

**Response (Final Diagnosis):**

```json
{
  "success": true,
  "data": {
    "status": "success",
    "diagnosis": [
      {
        "disease": "influenza",
        "certainty": 0.595
      },
      {
        "disease": "covid-19",
        "certainty": 0.42
      }
    ]
  }
}
```

### 3. Get Diagnosis

**POST** `/api/diagnose/result`

Retrieves the final diagnosis for a session.

**Request Body:**

- `sessionId` (string, required): The session ID

**Request:**

```bash
curl -X POST http://localhost:3000/api/diagnose/result \
  -H "Content-Type: application/json" \
  -d '{"sessionId": "a8f1dabc-9bac-4e2a-a12f-fd6447aaf5c7"}'
```

**Response:**

```json
{
  "success": true,
  "data": {
    "status": "success",
    "diagnosis": [
      {
        "disease": "influenza",
        "certainty": 0.595
      }
    ]
  }
}
```

### 4. End Session

**POST** `/api/diagnose/end`

Terminates a diagnosis session and frees up resources.

**Request Body:**

- `sessionId` (string, required): The session ID

**Request:**

```bash
curl -X POST http://localhost:3000/api/diagnose/end \
  -H "Content-Type: application/json" \
  -d '{"sessionId": "a8f1dabc-9bac-4e2a-a12f-fd6447aaf5c7"}'
```

**Response:**

```json
{
  "success": true,
  "message": "Session terminated successfully"
}
```

## Complete Example Flow

```bash
# 1. Start a session
SESSION_RESPONSE=$(curl -s -X POST http://localhost:3000/api/diagnose/start \
  -H "Content-Type: application/json")
SESSION_ID=$(echo $SESSION_RESPONSE | jq -r '.sessionId')

echo "Session ID: $SESSION_ID"

# 2. Answer questions
curl -X POST http://localhost:3000/api/diagnose/answer \
  -H "Content-Type: application/json" \
  -d "{\"sessionId\": \"$SESSION_ID\", \"symptom\": \"fever\", \"certainty\": 0.9}"

curl -X POST http://localhost:3000/api/diagnose/answer \
  -H "Content-Type: application/json" \
  -d "{\"sessionId\": \"$SESSION_ID\", \"symptom\": \"dry_cough\", \"certainty\": 0.8}"

# ... continue answering questions until diagnosis is returned

# 3. End the session (optional)
curl -X POST http://localhost:3000/api/diagnose/end \
  -H "Content-Type: application/json" \
  -d "{\"sessionId\": \"$SESSION_ID\"}"
```

## Error Responses

### Invalid Session

```json
{
  "success": false,
  "error": "Session not found",
  "message": "The session may have expired. Please start a new diagnosis."
}
```

### Invalid Input

```json
{
  "success": false,
  "error": "Invalid request",
  "message": "certainty must be between 0 and 1"
}
```

### Server Error

```json
{
  "success": false,
  "error": "Failed to process answer",
  "message": "Error details..."
}
```

## Session Management

- Sessions are automatically cleaned up after 5 minutes of inactivity
- Each session maintains a persistent Python process for state management
- Sessions can be manually terminated using the `/api/diagnose/end` endpoint
