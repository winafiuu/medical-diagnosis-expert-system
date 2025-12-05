# AI Medical Diagnosis Assistant

An interactive respiratory illness diagnosis system powered by an expert system using certainty factors and backward chaining.

## 🏗️ Tech Stack

- **Backend:** Node.js + Express.js
- **AI Core:** Python + Experta (Expert System Framework)
- **Frontend:** React.js + ShadCN UI + TailwindCSS + React Query + Zustand

## 📁 Project Structure

```
medical-diagnosis-expert-system/
├── backend/           # Node.js + Express API
│   └── src/
│       ├── routes/    # API route definitions
│       ├── controllers/ # Request handlers
│       └── services/  # Business logic & Python process management
├── frontend/          # React.js Application
│   └── src/
│       ├── components/ # Reusable UI components
│       ├── pages/     # Page components
│       ├── hooks/     # Custom React hooks
│       ├── store/     # Zustand state management
│       └── api/       # API service functions
├── ai-engine/         # Python Experta Engine
│   └── src/
│       ├── engine.py  # Main inference engine
│       ├── facts.py   # Fact definitions
│       └── rules/     # Disease rule definitions
└── docs/              # Documentation
```

## 🚀 Features

- **Interactive Chat Interface:** Conversational symptom collection
- **Certainty Factor Support:** Handle uncertainty in symptom reporting (0-100% confidence)
- **Backward Chaining:** Goal-driven question asking
- **Multiple Disease Detection:** Diagnoses various respiratory illnesses including:
  - Viral: Influenza, COVID-19, Common Cold
  - Bacterial: Strep Throat, Pneumonia, Bronchitis
- **Real-time Diagnosis:** Instant feedback with confidence scores

## 🔧 Setup Instructions

### Prerequisites

- Node.js (v16+)
- Python (v3.8+)
- npm or yarn

### Backend Setup

```bash
cd backend
npm install
npm run dev
```

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

### AI Engine Setup

```bash
cd ai-engine
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## 📝 Development Status

See [implementation-plan.md](./implementation-plan.md) for detailed development roadmap.

## ⚠️ Disclaimer

This is an educational project for university coursework. **This system is NOT a substitute for professional medical advice, diagnosis, or treatment.** Always consult with a qualified healthcare provider for medical concerns.

## 📄 License

Educational use only - University Course Project

## 👥 Contributors

Developed as part of an AI/Expert Systems course project.
