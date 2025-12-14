# AI Medical Diagnosis Assistant

An interactive respiratory illness diagnosis system powered by an expert system using certainty factors and backward chaining.

![Demo](https://img.shields.io/badge/status-completed-brightgreen) ![Node.js](https://img.shields.io/badge/Node.js-v16+-green) ![Python](https://img.shields.io/badge/Python-3.8+-blue) ![React](https://img.shields.io/badge/React-18+-61DAFB)

## 🏗️ Tech Stack

| Layer          | Technology                                                        |
| -------------- | ----------------------------------------------------------------- |
| **Frontend**   | React.js + Vite + ShadCN UI + TailwindCSS + React Query + Zustand |
| **Backend**    | Node.js + Express.js                                              |
| **AI Core**    | Python + Experta (Expert System Framework)                        |
| **Deployment** | Docker + Render                                                   |

## 📁 Project Structure

```
medical-diagnosis-expert-system/
├── backend/               # Node.js + Express API
│   └── src/
│       ├── routes/        # API route definitions
│       ├── controllers/   # Request handlers
│       └── services/      # Business logic & Python process management
├── frontend/              # React.js Application
│   └── src/
│       ├── components/    # Reusable UI components
│       ├── pages/         # Page components
│       ├── hooks/         # Custom React hooks
│       ├── store/         # Zustand state management
│       └── api/           # API service functions
├── ai-engine/             # Python Experta Engine
│   └── src/
│       ├── engine.py      # Main inference engine
│       ├── facts.py       # Fact definitions
│       ├── cf_utils.py    # Certainty Factor utilities
│       └── rules/         # Disease rule definitions
│           ├── viral_rules.py     # Influenza, COVID-19, Common Cold
│           └── bacterial_rules.py # Strep Throat, Pneumonia, Bronchitis
├── docs/                  # Documentation
│   ├── implementation-plan.md     # Step-by-step implementation guide
│   ├── project_explanation.md     # Detailed project architecture
│   ├── DEPLOYMENT.md              # Render deployment guide
│   ├── API_TESTING.md             # API testing documentation
│   ├── STDIN_STDOUT_API.md        # Python engine API specification
│   └── BACTERIAL_RULES_README.md  # Bacterial rules documentation
├── others/                # Project Resources
│   ├── presentation.pptx  # Presentation slides
│   ├── demo.mp4           # Video demonstration
│   └── report.pdf         # Project report
├── Dockerfile             # Container configuration
└── render.yaml            # Render Blueprint deployment config
```

## 🚀 Features

- **Interactive Chat Interface:** Conversational symptom collection with a modern UI
- **Certainty Factor Support:** Handle uncertainty in symptom reporting (0-100% confidence)
- **Backward Chaining:** Goal-driven question asking for efficient diagnosis
- **Multiple Disease Detection:** Diagnoses various respiratory illnesses including:
  - **Viral:** Influenza, COVID-19, Common Cold
  - **Bacterial:** Strep Throat, Pneumonia, Bronchitis
- **Real-time Diagnosis:** Instant feedback with confidence scores
- **Responsive Design:** Mobile-friendly chat interface
- **One-Click Deployment:** Deploy to Render with Blueprint configuration

## 🔧 Local Development Setup

### Prerequisites

- Node.js (v16+)
- Python (v3.8+)
- npm or yarn

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd medical-diagnosis-expert-system
```

### 2. Backend Setup

```bash
cd backend
npm install
npm run dev
```

The backend runs on `http://localhost:3000`.

### 3. Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

The frontend runs on `http://localhost:5173`.

### 4. AI Engine Setup

```bash
cd ai-engine
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## 🐳 Docker Deployment

Build and run the entire backend + AI engine in a single container:

```bash
docker build -t medical-diagnosis-api .
docker run -p 3000:3000 medical-diagnosis-api
```

## ☁️ Cloud Deployment (Render)

This project includes a `render.yaml` Blueprint for easy deployment to Render:

1. Push your code to a Git repository
2. Create a new **Blueprint** in Render
3. Connect your repository
4. Set the `VITE_API_URL` environment variable for the frontend

For detailed instructions, see [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md).

## 📚 Documentation

| Document                                           | Description                       |
| -------------------------------------------------- | --------------------------------- |
| [Project Explanation](docs/project_explanation.md) | Architecture and design decisions |
| [Deployment Guide](docs/DEPLOYMENT.md)             | Render deployment instructions    |
| [API Testing](docs/API_TESTING.md)                 | API endpoint testing guide        |
| [STDIN/STDOUT API](docs/STDIN_STDOUT_API.md)       | Python engine communication spec  |

## 🔌 API Endpoints

| Endpoint               | Method | Description                                        |
| ---------------------- | ------ | -------------------------------------------------- |
| `/health`              | GET    | Health check endpoint                              |
| `/api/diagnose/start`  | POST   | Start a new diagnosis session                      |
| `/api/diagnose/answer` | POST   | Submit symptom answer and get next question/result |

## 🧠 How It Works

1. **User starts a diagnosis session** → Backend spawns Python AI engine
2. **AI engine asks questions** → Based on backward chaining logic
3. **User provides symptoms with certainty** → 0-100% confidence slider
4. **AI combines evidence** → Using Certainty Factor calculations
5. **Diagnosis is generated** → With confidence scores for each possible condition

### Certainty Factor Logic

- **AND Logic:** `min(CF1, CF2)` - Both symptoms required
- **OR Logic:** `max(CF1, CF2)` - Either symptom sufficient
- **Rule Confidence:** `Final_CF = Combined_Evidence_CF × Rule_Reliability_CF`

## 🔗 Other Resources

| Resource                   | Online Link                                                                           | Local File                                    |
| -------------------------- | ------------------------------------------------------------------------------------- | --------------------------------------------- |
| 🌐 **Live Website**        | [medical-diagnosis-web.onrender.com](https://medical-diagnosis-web.onrender.com/)     | -                                             |
| 📊 **Presentation Slides** | [View on Canva](https://www.canva.com/design/DAG7aJsxHE0/Z09988A-A2yx6l5dKawi4g/edit) | [presentation.pptx](others/presentation.pptx) |
| 🎥 **Video Demo**          | [Watch on Loom](https://www.loom.com/share/a40c4501ecbe4f4eb6a55d322789b772)          | [demo.mp4](others/demo.mp4)                   |
| 📄 **Project Report**      | -                                                                                     | [report.pdf](others/report.pdf)               |

## ⚠️ Disclaimer

> **This is an educational project for university coursework.**
>
> **This system is NOT a substitute for professional medical advice, diagnosis, or treatment.** Always consult with a qualified healthcare provider for medical concerns.

## 📄 License

Educational use only - University Course Project
