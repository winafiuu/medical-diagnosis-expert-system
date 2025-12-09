# Medical Diagnosis Expert System - Project Deep Dive

This document provides a detailed technical analysis of the "Interactive Respiratory Illness Diagnosis System". It explains the architecture, data flow, and implementation details of the 3-tier headless application.

## 1. High-Level Architecture

The system is built on a **3-Tier Headless Architecture**, designed to separate concerns between the user interface, the server-side orchestration, and the AI inference logic.

| Tier          | Technology                | Function                                                                      |
| :------------ | :------------------------ | :---------------------------------------------------------------------------- |
| **Frontend**  | React + TypeScript + Vite | Handles user interaction, chat UI, state management (Zustand).                |
| **Backend**   | Node.js + Express         | Orchestrates sessions, manages Python child processes, exposes REST API.      |
| **AI Engine** | Python + Experta          | Runs the Expert System rules, handles certainty factors, generates questions. |

---

## 2. Detailed Component Breakdown

### A. Frontend (client-side)

**Location:** `frontend/`

The frontend is a **Single Page Application (SPA)** built with React. It provides a chat-like interface where users answer questions to get a diagnosis.

- **State Management (`diagnosisStore.ts`)**: Uses **Zustand** to store the global application state.
  - `sessionId`: Unique token for the current diagnosis session.
  - `messages`: History of the chat (User answers and System questions).
  - `currentQuestion`: The active question displayed to the user.
  - `diagnosisResult`: Final results when the session ends.
- **API Layer (`api/diagnosis.ts`)**: Handles HTTP communication with the backend.
  - `startDiagnosis()`: Initiates a session.
  - `submitAnswer()`: Sends user input (symptom + certainty).
- **UI Components**:
  - `ChatContainer`: The main wrapper.
  - `SymptomSlider`: Allows users to input certainty (0-100%).

### B. Backend (Server-side)

**Location:** `backend/`

The backend acts as a bridge and **Session Manager**. Since HTTP is stateless, but the AI conversation is stateful, the backend must maintain the link between a User and their specific Python AI process.

- **API Routes (`diagnosisController.js`)**: Endpoints like `/start` and `/answer` that forward requests to the service layer.
- **Session Manager (`sessionManager.js`)**: **CRITICAL COMPONENT**.
  - Maintains a `Map<sessionId, DiagnosisSession>`.
  - **Architecture**: For _each_ active diagnosis session, it spawns a **dedicated persistent Python child process**.
  - It manages the lifecycle: creating the process, piping inputs to `stdin`, reading outputs from `stdout`, and killing idle processes.
- **Python Service (`pythonService.js`)**: Wrapper for node's `child_process.spawn`.

### C. AI Engine (The Brain)

**Location:** `ai-engine/`

The core intelligence is a Python script that runs an **Expert System** using the `experta` library (a CLIPS wrapper).

- **Entry Point (`main.py`)**:
  - Runs an infinite loop reading JSON commands from `stdin`.
  - Handles actions: `start`, `add_symptom`, `get_diagnosis`.
  - Outputs JSON responses to `stdout`.
  - **Persistent State**: The `engine` object stays alive in memory for the duration of the process.
- **Inference Engine (`src/engine.py`)**:
  - Inherits from `KnowledgeEngine` and various Rule classes (e.g., `InfluenzaRules`, `BacterialRules`).
  - **Forward Chaining**: When a fact (symptom) is added, rules automatically fire to update diagnosis certainty.
- **Question Engine (`src/question_engine.py`)**:
  - **Simulated Backward Chaining**: Instead of just waiting for data, it actively decides what to ask next.
  - **Algorithm**: It calculates **Information Gain** for potential questions.
    - It considers the "discrimination score" (how well a symptom splits component diseases).
    - It prioritizes relevant symptoms for the top current diagnosis candidates.

---

## 3. The Data Flow (Lifecycle of a Request)

Here is exactly what happens when a user clicks "Start Diagnosis":

1.  **Frontend**: Calls `POST /api/diagnose/start`.
2.  **Backend**:
    - `SessionManager` generates a UUID (`sessionId`).
    - Spawns a new process: `python3 ai-engine/main.py`.
    - Sends JSON to process stdin: `{"action": "start"}`.
3.  **AI Engine**:
    - `main.py` receives `start`.
    - Calls `engine.get_initial_question()` (usually "Fever").
    - Prints JSON: `{"status": "success", "next_question": {...}}`.
4.  **Backend**: Returns `sessionId` and question to Frontend.

**When User Answers:**

1.  **Frontend**: Calls `POST /api/diagnose/answer` with `{sessionId, symptom: "fever", certainty: 0.8}`.
2.  **Backend**:
    - Looks up the running process using `sessionId`.
    - Pipes to stdin: `{"action": "add_symptom", "symptom": "fever", "certainty": 0.8}`.
3.  **AI Engine**:
    - `engine.add_symptom("fever", 0.8)` -> Adds Fact to Experta system.
    - `engine.run()` -> **Rules Fire!** (e.g., "If fever, could be Flu (0.7 CF)").
    - `engine.should_continue_asking()`: Checks if confidence threshold is met or max questions reached.
    - **Next Question**: `question_engine` picks the next best question based on the new state.
    - Returns JSON response.
4.  **Frontend**: Updates UI with new question or final result.

---

## 4. Key Algorithms & Logic

### Certainty Factors (CF)

The system handles uncertainty using Shortliffe's Certainty Factor model (used in MYCIN).

- **Input**: Users provide CF (0.0 to 1.0).
- **AND Logic**: `min(cf1, cf2)` (e.g., fever AND cough).
- **OR Logic**: `max(cf1, cf2)` (e.g., multiple rules pointing to same disease).
- **Rule Reliability**: `Final_CF = rules_reliability * min(evidence_cfs)`.

### Question Selection (Information Gain)

The system tries to be smart about what it asks.

- **Priority Scores**: Hardcoded importance for distinguishing symptoms (e.g., "Loss of smell" is high priority for COVID).
- **Dynamic Selection**: It filters questions to those relevant to the _current top diagnoses_. It stops asking about "Strep Throat" if the probability drops near zero.

---

## 5. File Usage & Purpose

| File Path                                | Purpose                                                           |
| :--------------------------------------- | :---------------------------------------------------------------- |
| `ai-engine/main.py`                      | CLI Interface for the AI. Handles I/O parsing.                    |
| `ai-engine/src/engine.py`                | The specific `KnowledgeEngine` subclass combining all rules.      |
| `ai-engine/src/question_engine.py`       | Logic for determining the next best question.                     |
| `backend/src/services/sessionManager.js` | Manages persistent Python processes (Creation, Timeout, Cleanup). |
| `frontend/src/store/diagnosisStore.ts`   | Zustand store holding the chat history and session ID.            |
