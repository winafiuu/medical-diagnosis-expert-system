# Implementation Plan: AI Medical Diagnosis Assistant

> **Tech Stack:**
>
> - **Backend:** Node.js + Express.js
> - **AI Core:** Python + Experta
> - **Frontend:** React.js + ShadCN + TailwindCSS + React Query + Zustand

---

## ⚠️ Implementation Workflow Requirements

**CRITICAL: Follow these rules for EVERY step:**

1. ✅ **Mark Completed Tasks**: Update this implementation plan file by checking off `[x]` all completed tasks after finishing each step
2. 🛑 **Wait for Permission**: After completing a step, STOP and ask the user for permission before proceeding to the next step
3. 📊 **Update Progress Tracker**: Update the progress tracker table at the bottom when a phase changes status

**Do NOT proceed to the next step without explicit user confirmation!**

---

## Phase 1: Project Setup & Foundation

### Step 1: Initialize Project Structure

- [x] Create the main project directory structure:
  ```
  medical-diagnosis-expert-system/
  ├── backend/           # Node.js + Express API
  ├── frontend/          # React.js Application
  ├── ai-engine/         # Python Experta Engine
  └── docs/              # Documentation
  ```
- [x] Initialize Git repository and create `.gitignore`
- [x] Create README.md with project overview

---

### Step 2: Backend Foundation (Node.js + Express)

- [x] Initialize Node.js project with `npm init`
- [x] Install dependencies:
  - `express` - Web framework
  - `cors` - Cross-origin resource sharing
  - `dotenv` - Environment variables
  - `nodemon` (dev) - Auto-restart server
- [x] Create basic Express server structure:
  - `backend/src/index.js` - Entry point
  - `backend/src/routes/` - API routes
  - `backend/src/controllers/` - Request handlers
  - `backend/src/services/` - Business logic

---

### Step 3: Frontend Foundation (React + TailwindCSS + ShadCN)

- [x] Initialize React project with Vite
- [x] Install and configure TailwindCSS
- [x] Install and configure ShadCN UI components
- [x] Install state management & data fetching:
  - `zustand` - State management
  - `@tanstack/react-query` - Server state management
  - `axios` - HTTP client
- [x] Create basic folder structure:
  - `frontend/src/components/` - Reusable components
  - `frontend/src/pages/` - Page components
  - `frontend/src/hooks/` - Custom hooks
  - `frontend/src/store/` - Zustand stores
  - `frontend/src/api/` - API service functions

---

### Step 4: AI Engine Foundation (Python + Experta)

- [x] Create Python virtual environment
- [x] Install dependencies:
  - `experta` - Expert system framework
- [x] Create basic folder structure:
  - `ai-engine/src/engine.py` - Main inference engine
  - `ai-engine/src/facts.py` - Fact definitions
  - `ai-engine/src/rules/` - Rule definitions
  - `ai-engine/main.py` - Entry point (stdin/stdout interface)

---

## Phase 2: Core AI Engine Development

### Step 5: Define Facts & Knowledge Representation

- [ ] Create symptom facts (Fever, Cough, Fatigue, etc.)
- [ ] Create disease facts (Influenza, COVID-19, Pneumonia, etc.)
- [ ] Implement Certainty Factor (CF) support in facts
- [ ] Create base classes for symptom and diagnosis facts

---

### Step 6: Implement Certainty Factor Logic

- [ ] Implement CF calculation utilities:
  - AND logic: `min(CF1, CF2)`
  - OR logic: `max(CF1, CF2)`
  - Rule confidence: `Final_CF = Combined_Evidence_CF * Rule_Reliability_CF`
- [ ] Create CF combination functions

---

### Step 7: Implement Viral Disease Rules (Knowledge Lead A)

- [ ] Research medical data for viral illnesses
- [ ] Implement rules for:
  - **Influenza (Flu)** - Symptoms: fever, body aches, fatigue, cough
  - **COVID-19** - Symptoms: fever, dry cough, loss of taste/smell, fatigue
  - **Common Cold** - Symptoms: runny nose, sneezing, mild cough, sore throat
- [ ] Add CF weights to each rule based on medical reliability

---

### Step 8: Implement Bacterial Disease Rules (Knowledge Lead B)

- [ ] Research medical data for bacterial illnesses
- [ ] Implement rules for:
  - **Strep Throat** - Symptoms: severe sore throat, fever, swollen lymph nodes
  - **Pneumonia** - Symptoms: high fever, chest pain, productive cough, shortness of breath
  - **Bronchitis** - Symptoms: persistent cough, chest discomfort, mucus production
- [ ] Add CF weights to each rule based on medical reliability

---

### Step 9: Implement Question-Asking Logic (Backward Chaining Simulation)

- [ ] Implement goal-driven question generation
- [ ] Create salience-based rule priorities
- [ ] Implement dynamic question selection based on previous answers
- [ ] Create mapping between internal symptom names and user-friendly questions

---

### Step 10: Create stdin/stdout Interface

- [ ] Implement JSON input parsing from stdin
- [ ] Create response format for:
  - Next question to ask
  - Final diagnosis with CF scores
- [ ] Add error handling for invalid inputs

---

## Phase 3: Backend API Development

### Step 11: Implement Python Process Management

- [ ] Create service for spawning Python child process
- [ ] Implement stdin/stdout communication
- [ ] Add proper error handling and timeouts

---

### Step 12: Create Diagnosis API Endpoints

- [ ] Implement `/api/diagnose/start` - Initialize a diagnosis session
- [ ] Implement `/api/diagnose/answer` - Submit answer and get next question or result
- [ ] Add request validation and error handling

---

## Phase 4: Frontend Development

### Step 13: Setup State Management (Zustand)

- [ ] Create diagnosis store:
  - Chat message history
  - Current question
  - Diagnosis result
- [ ] Create loading/error states

---

### Step 14: Setup API Layer (React Query + Axios)

- [ ] Create Axios instance with base configuration
- [ ] Implement API hooks:
  - `useStartDiagnosis` - Start new session
  - `useSubmitAnswer` - Submit symptom response
- [ ] Add error handling

---

### Step 15: Build Chat Interface Components

- [ ] Create base chat components using ShadCN:
  - `ChatContainer` - Main chat wrapper
  - `ChatMessage` - Individual message bubble
  - `ChatInput` - User input area
  - `SymptomSlider` - CF input (0-100% certainty slider)
  - `QuickResponseButtons` - Yes/No/Unsure buttons
- [ ] Style components with TailwindCSS

---

### Step 16: Build Diagnosis Result Components

- [ ] Create result display components:
  - `DiagnosisCard` - Main result card
  - `ConfidenceBar` - Visual CF representation
  - `DisclaimerBanner` - Medical disclaimer
- [ ] Create "Start New Diagnosis" functionality

---

### Step 17: Build Main Application Layout

- [ ] Create main application layout:
  - Header with app title
  - Chat interface area
  - Result display area
- [ ] Implement basic routing (Home → Diagnosis → Result)

---

### Step 18: Implement Chat Flow Logic

- [ ] Connect frontend to backend API
- [ ] Implement message flow:
  1. Display system greeting
  2. Show first question
  3. Capture user response with CF
  4. Send to backend, receive next question
  5. Repeat until diagnosis complete
  6. Display final result
- [ ] Handle loading and error states

---

## Progress Tracker

| Phase                  |     Status     | Completion |
| :--------------------- | :------------: | :--------: |
| Phase 1: Project Setup |  🟢 Completed  |    100%    |
| Phase 2: AI Engine     | 🔴 Not Started |     0%     |
| Phase 3: Backend API   | 🔴 Not Started |     0%     |
| Phase 4: Frontend      | 🔴 Not Started |     0%     |

---

> **Legend:**
>
> - 🔴 Not Started
> - 🟡 In Progress
> - 🟢 Completed
> - [ ] Task pending
> - [x] Task completed

---

## Notes

- Each step should be completed and marked as done before proceeding to the next
- Wait for confirmation signal before starting the next step
- This is a university course project - focus on core functionality
