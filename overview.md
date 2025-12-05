# Project Design Document: AI Medical Diagnosis Assistant

**Project Title:** Interactive Respiratory Illness Diagnosis System
**Course:** Artificial Intelligence
**Team Size:** 4 Members
**Duration:** 7 Weeks

---

## 1. Executive Summary

Our team is building an **interactive AI medical diagnosis assistant** that functions as a web-based chatbot. The system is designed to diagnose common respiratory illnesses (such as Influenza, COVID-19, and Pneumonia) by mimicking the reasoning of a human doctor. It engages the user in a dynamic question-and-answer session, deciding which question to ask next based on previous answers.

The core intelligence is a rule-based **Expert System** utilizing **goal-driven logic** and **Certainty Factors (CF)** to handle user uncertainty (e.g., "I am 80% sure I have a fever"). The application uses a decoupled architecture, with a Node.js backend serving a user-friendly chat interface and orchestrating a specialized Python AI engine.

---

## 2. Team Roles & Responsibilities

| Role | Responsibility | Focus Area |
| :--- | :--- | :--- |
| **Project Lead** | **Full-Stack Application & Integration** | Builds the web frontend, the Node.js API, and handles the "plumbing" to connect the AI engine. Manages the repo and report. |
| **Inference Lead** | **AI Core Engineering** | Builds the `experta` engine framework. Implements the backward-chaining simulation (Q&A logic) and the math for Certainty Factors. |
| **Knowledge Lead A** | **Domain Expert (Viral)** | Researches medical data and implements diagnostic rules for **Viral Illnesses** (Flu, COVID-19, Common Cold). |
| **Knowledge Lead B** | **Domain Expert (Bacterial)** | Researches medical data and implements diagnostic rules for **Bacterial Illnesses** (Strep Throat, Pneumonia, Bronchitis). |

---

## 3. Technical Architecture

The system follows a **3-Tier "Headless" Architecture**. This ensures a clear separation of concerns between the user interface, the server logic, and the artificial intelligence.

### A. The Frontend (Client-Side)
* **Type:** Single Page Application (SPA) / Chat Interface.
* **Function:** Displays the chat window, captures user input, and displays the final diagnosis.
* **Communication:** Sends JSON data to the Backend via HTTP `POST`.

### B. The Backend (Server-Side)
* **Type:** REST API.
* **Function:** Acts as the central coordinator. It serves the static frontend files and exposes an API endpoint (`/api/diagnose`). It manages the lifecycle of the Python process.
* **Integration:** Uses the `child_process` module to spawn the Python AI script for every diagnosis request.

### C. The AI Core (Inference Layer)
* **Type:** Command-Line Script.
* **Function:** The "brain" of the operation. It receives symptom data via `stdin`, runs the inference engine, and outputs the result via `stdout`.

> **System Architecture Diagram**
>
> `[Frontend (Browser)]`  <-->  `[Node.js Backend (Express API)]`  <-->  `[Python Child Process (Experta AI)]`
>
> 1. Frontend sends User Input (JSON) to Node.js.
> 2. Node.js spawns Python script and pipes Input.
> 3. Python runs Logic/Rules and prints Diagnosis (JSON) to stdout.
> 4. Node.js captures stdout and sends Response back to Frontend.

---

## 4. Detailed Tech Stack

### Artificial Intelligence (The Core)
* **Language:** Python 3.x
* **Library:** **`experta`** (A Python implementation of the CLIPS rule engine).
* **Key Concepts:**
    * **Knowledge Representation:** Production Rules (`IF-THEN`).
    * **Inference Strategy:** Simulation of Backward Chaining (Goal-Driven) using `salience` priorities.
    * **Heuristics:** Certainty Factors (CF) to calculate confidence scores (0.0 - 1.0).

### Backend (The API)
* **Runtime:** Node.js
* **Framework:** **Express.js** (Lightweight web server).
* **Process Management:** Node.js native `child_process.spawn`.

### Frontend (The UI)
* **Languages:** HTML5, CSS3, Vanilla JavaScript (ES6+).
* **Style:** Custom CSS (Chat-bubble interface).

### Tools & DevOps
* **Version Control:** Git & GitHub.
* **Testing:** Postman (for API testing), PyTest (for engine logic).

---

## 5. AI Methodology

The project strictly adheres to the AI principles outlined in the course requirements:

1.  **Logic Programming:** We rely on declarative rules (`@Rule`) rather than imperative code logic.
2.  **Inference Rules:**
    * **Goal-Driven (Simulated Backward Chaining):** The system has a high-level goal ("Find Diagnosis"). It triggers rules to "ask" for missing facts (symptoms) dynamically.
    * **Data-Driven (Forward Chaining):** Once facts are gathered, diagnostic rules fire automatically to produce a conclusion.
3.  **Handling Uncertainty:**
    * User inputs are not boolean (`True/False`). They are floats (`0.0` to `1.0`).
    * **AND Logic:** Uses `min(CF1, CF2)`.
    * **OR Logic:** Uses `max(CF1, CF2)`.
    * **Rule Confidence:** `Final_CF = Combined_Evidence_CF * Rule_Reliability_CF`.

---

## 6. Implementation Plan (7 Weeks)

* **Week 1: Research & Design.** (No code). Defining scope, finding medical sources, and designing the integration architecture.
* **Week 2: Component Prototyping.** Building the v1 AI Core (Python), the v1 API (Node.js), and formalizing the written rules.
* **Week 3: Integration ("First Light").** Connecting the Node.js API to the Python script. First successful end-to-end diagnosis.
* **Week 4: Feature Expansion.** Implementing complex logic (`OR` rules) and expanding the Knowledge Base to cover all illnesses.
* **Week 5: Feature Lock.** Finalizing the UI and API. System becomes feature-complete.
* **Week 6: Tuning & Drafting.** Aggressive testing. Tuning Certainty Factors for accuracy. Drafting the final report.
* **Week 7: Delivery.** Final code freeze, report submission, and presentation rehearsal.