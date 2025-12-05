# AI Engine - Medical Diagnosis Expert System

This directory contains the Python-based AI engine using the Experta framework for medical diagnosis.

## Structure

```
ai-engine/
├── src/
│   ├── engine.py          # Main inference engine
│   ├── facts.py           # Fact definitions
│   └── rules/             # Disease rule definitions
│       ├── __init__.py
│       ├── viral_rules.py      # (To be implemented)
│       └── bacterial_rules.py  # (To be implemented)
├── main.py                # Entry point with stdin/stdout interface
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## Setup

### Option 1: Using Virtual Environment (Recommended)

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # On Linux/Mac
# or
venv\Scripts\activate  # On Windows

# Install dependencies
pip install -r requirements.txt
```

### Option 2: System-wide Installation

```bash
pip install -r requirements.txt
```

## Usage

The AI engine communicates via stdin/stdout using JSON messages.

### Starting a Session

```bash
echo '{"action": "start"}' | python main.py
```

### Adding a Symptom

```bash
echo '{"action": "add_symptom", "symptom": "fever", "certainty": 0.8}' | python main.py
```

### Getting Diagnosis

```bash
echo '{"action": "get_diagnosis"}' | python main.py
```

## Input Format

```json
{
  "action": "start" | "add_symptom" | "get_diagnosis",
  "symptom": "symptom_name",  // for add_symptom
  "certainty": 0.8            // for add_symptom (0.0 to 1.0)
}
```

## Output Format

```json
{
  "status": "success" | "error",
  "next_question": {
    "symptom": "fever",
    "text": "Do you have a fever?"
  },
  "diagnosis": [
    {"disease": "Influenza", "certainty": 0.85}
  ],
  "message": "Status or error message"
}
```

## Certainty Factor Logic

- **AND logic**: `min(CF1, CF2)` - Used when multiple symptoms must be present
- **OR logic**: `max(CF1, CF2)` - Used when any symptom can indicate a condition
- **Rule confidence**: `Final_CF = Evidence_CF × Rule_Reliability_CF`

## Development Status

- [x] Basic engine structure
- [x] Fact definitions
- [x] Certainty factor logic
- [x] stdin/stdout interface
- [ ] Viral disease rules
- [ ] Bacterial disease rules
- [ ] Question-asking logic
