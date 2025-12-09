# AI Engine stdin/stdout Interface Documentation

## Overview

The AI diagnosis engine provides a JSON-based stdin/stdout interface for communication with the Node.js backend. This allows the backend to spawn a Python process and communicate with it via standard input/output streams.

## Communication Protocol

### Input Format

All commands must be sent as **single-line JSON objects** followed by a newline character (`\n`).

```json
{ "action": "start" }
```

### Output Format

All responses are returned as **single-line JSON objects** followed by a newline character.

```json
{ "status": "success", "message": "..." }
```

---

## Actions

### 1. Start Diagnosis Session

**Action:** `start`

Initializes a new diagnosis session and returns the first question.

#### Request

```json
{
  "action": "start"
}
```

#### Response (Success)

```json
{
  "status": "success",
  "message": "Diagnosis session started",
  "next_question": {
    "symptom": "fever",
    "text": "Do you have a fever (elevated body temperature)?"
  }
}
```

---

### 2. Add Symptom

**Action:** `add_symptom`

Records a symptom with a certainty factor and returns either the next question or a diagnosis.

#### Request

```json
{
  "action": "add_symptom",
  "symptom": "fever",
  "certainty": 0.8
}
```

**Parameters:**

- `symptom` (string, required): The internal name of the symptom (e.g., `"fever"`, `"cough"`, `"body_aches"`)
- `certainty` (number, optional): Certainty factor between 0.0 and 1.0. Defaults to 1.0 if not provided.

#### Response (More Questions)

```json
{
  "status": "success",
  "message": "Symptom recorded",
  "next_question": {
    "symptom": "cough",
    "text": "Do you have a cough?"
  }
}
```

#### Response (Diagnosis Ready)

```json
{
  "status": "success",
  "diagnosis": [
    { "disease": "Influenza", "certainty": 0.85 },
    { "disease": "COVID-19", "certainty": 0.65 },
    { "disease": "Common Cold", "certainty": 0.45 }
  ]
}
```

**Note:** The diagnosis list is sorted by certainty in descending order.

---

### 3. Get Diagnosis

**Action:** `get_diagnosis`

Forces the engine to return a diagnosis based on current symptoms, even if more questions could be asked.

#### Request

```json
{
  "action": "get_diagnosis"
}
```

#### Response

```json
{
  "status": "success",
  "diagnosis": [
    { "disease": "Influenza", "certainty": 0.85 },
    { "disease": "COVID-19", "certainty": 0.65 }
  ]
}
```

---

## Error Handling

All errors return a response with `"status": "error"`, an error message, and an error code.

### Error Response Format

```json
{
  "status": "error",
  "message": "Human-readable error message",
  "error_code": "ERROR_CODE"
}
```

### Error Codes

| Error Code               | Description                                    | Example                                       |
| ------------------------ | ---------------------------------------------- | --------------------------------------------- |
| `INVALID_JSON`           | The input is not valid JSON                    | `"not json"`                                  |
| `INVALID_ACTION`         | Unknown action specified                       | `{"action": "delete"}`                        |
| `MISSING_SYMPTOM`        | Symptom parameter is required but not provided | `{"action": "add_symptom", "certainty": 0.8}` |
| `INVALID_CERTAINTY_TYPE` | Certainty must be a number                     | `{"certainty": "high"}`                       |
| `CERTAINTY_OUT_OF_RANGE` | Certainty must be between 0.0 and 1.0          | `{"certainty": 1.5}`                          |
| `INTERNAL_ERROR`         | Unexpected internal error                      | Various causes                                |

### Example Error Responses

#### Invalid JSON

```json
{
  "status": "error",
  "message": "Invalid JSON input: Expecting value: line 1 column 1 (char 0)",
  "error_code": "INVALID_JSON"
}
```

#### Invalid Action

```json
{
  "status": "error",
  "message": "Unknown action: delete_symptom. Valid actions are: start, add_symptom, get_diagnosis",
  "error_code": "INVALID_ACTION"
}
```

#### Missing Symptom

```json
{
  "status": "error",
  "message": "Symptom name is required",
  "error_code": "MISSING_SYMPTOM"
}
```

#### Invalid Certainty Type

```json
{
  "status": "error",
  "message": "Certainty must be a number, got str",
  "error_code": "INVALID_CERTAINTY_TYPE"
}
```

#### Certainty Out of Range

```json
{
  "status": "error",
  "message": "Certainty must be between 0.0 and 1.0, got 1.5",
  "error_code": "CERTAINTY_OUT_OF_RANGE"
}
```

---

## Usage Example (Node.js)

```javascript
const { spawn } = require('child_process')

// Spawn the Python process
const pythonProcess = spawn('python3', ['ai-engine/main.py'])

// Handle stdout
pythonProcess.stdout.on('data', (data) => {
  const response = JSON.parse(data.toString())
  console.log('Response:', response)
})

// Send a command
function sendCommand(command) {
  pythonProcess.stdin.write(JSON.stringify(command) + '\n')
}

// Start a diagnosis session
sendCommand({ action: 'start' })

// Add a symptom
sendCommand({
  action: 'add_symptom',
  symptom: 'fever',
  certainty: 0.9,
})

// Get diagnosis
sendCommand({ action: 'get_diagnosis' })
```

---

## Symptom Names

The following symptom names are recognized by the system:

### General Symptoms

- `fever` - Elevated body temperature
- `fatigue` - Tiredness, lack of energy
- `headache` - Head pain

### Respiratory Symptoms

- `cough` - Dry or productive cough
- `productive_cough` - Cough with mucus/phlegm
- `dry_cough` - Cough without mucus
- `shortness_of_breath` - Difficulty breathing
- `chest_pain` - Pain in chest area
- `chest_discomfort` - Discomfort in chest

### Upper Respiratory Symptoms

- `sore_throat` - Throat pain
- `severe_sore_throat` - Intense throat pain
- `runny_nose` - Nasal discharge
- `sneezing` - Frequent sneezing
- `nasal_congestion` - Stuffy nose

### COVID-19 Specific

- `loss_of_taste` - Loss of taste sensation
- `loss_of_smell` - Loss of smell sensation

### Flu-like Symptoms

- `body_aches` - Muscle aches and pains
- `chills` - Feeling cold, shivering

### Other Symptoms

- `swollen_lymph_nodes` - Enlarged lymph nodes
- `mucus_production` - Production of mucus/phlegm
- `difficulty_swallowing` - Trouble swallowing

---

## Testing

### Run Basic Interface Test

```bash
cd ai-engine
python3 test_stdin_interface.py
```

### Run Validation Test

```bash
cd ai-engine
python3 test_validation.py
```

---

## Notes

1. **Stateful Session**: The engine maintains state between commands. Always start with `action: "start"` for a new diagnosis.

2. **Certainty Factors**: Use values between 0.0 (no certainty) and 1.0 (complete certainty). For yes/no questions:

   - Yes = 1.0
   - No = 0.0
   - Unsure = 0.5

3. **Question Flow**: The engine uses intelligent question selection based on current diagnosis probabilities. It will ask the most relevant questions first.

4. **Graceful Shutdown**: The process can be terminated with SIGTERM or by closing stdin.

5. **Output Buffering**: All output is flushed immediately (`flush=True`) to ensure real-time communication.
