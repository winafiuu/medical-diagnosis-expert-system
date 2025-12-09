# Bacterial Disease Rules - Quick Reference

## Overview

This module implements diagnostic rules for three bacterial respiratory illnesses using the Experta expert system framework.

## Diseases Covered

### 1. Strep Throat (Streptococcal Pharyngitis)

**Caused by:** Group A Streptococcus bacteria

**Key Symptoms:**

- Severe sore throat
- Fever
- Swollen lymph nodes (neck)
- Difficulty swallowing
- **Absent:** Cough, runny nose, sneezing

**Rules Implemented:** 3

- Classic presentation (CF: 0.85)
- Moderate presentation (CF: 0.75)
- Mild presentation (CF: 0.65)

---

### 2. Pneumonia

**Caused by:** Various bacteria (commonly Streptococcus pneumoniae)

**Key Symptoms:**

- High fever (>101°F)
- Chest pain (especially when breathing)
- Productive cough (mucus/phlegm)
- Shortness of breath

**Rules Implemented:** 4

- Classic presentation (CF: 0.90)
- Respiratory focus (CF: 0.80)
- With chest pain (CF: 0.75)
- Moderate presentation (CF: 0.70)

---

### 3. Bronchitis (Acute Bacterial Bronchitis)

**Caused by:** Various bacteria (often following viral infection)

**Key Symptoms:**

- Persistent cough
- Chest discomfort
- Mucus production
- Fatigue
- **Absent:** High fever (distinguishes from pneumonia)

**Rules Implemented:** 5

- Classic presentation (CF: 0.80)
- With fatigue (CF: 0.75)
- Cough and mucus (CF: 0.70)
- With wheezing (CF: 0.70)
- Mild presentation (CF: 0.65)

## Rule Design Principles

### 1. Salience (Priority)

Rules are prioritized based on specificity:

- **115**: Pneumonia classic (most specific, 4 symptoms)
- **105**: Strep throat classic (4 symptoms)
- **95-100**: Moderate presentations (3 symptoms)
- **80-90**: Mild presentations (2 symptoms)
- **70**: Minimal presentations

### 2. Certainty Factors

Each rule has two CF components:

1. **Evidence CF**: Minimum of all symptom certainties (AND logic)
2. **Rule Confidence**: Reliability of the rule itself (0.65-0.90)

Final CF = Evidence CF × Rule Confidence

### 3. Negative Indicators

Rules check for **absence** of symptoms to improve specificity:

- Strep throat: No cough, runny nose, or sneezing
- Bronchitis: No high fever (< 0.7)

### 4. Symptom Thresholds

Minimum certainty requirements prevent false positives:

- Primary symptoms: 0.6-0.8
- Supporting symptoms: 0.4-0.5
- Negative indicators: < 0.3-0.4

## Testing

Run the test suite:

```bash
cd ai-engine
source venv/bin/activate
python test_bacterial_rules.py
```

Expected results:

- Strep throat: ~60% confidence with classic symptoms
- Pneumonia: ~63% confidence with classic symptoms
- Bronchitis: ~56% confidence with classic symptoms

## Integration

The bacterial rules are integrated into the main `MedicalDiagnosisEngine`:

```python
from src.engine import MedicalDiagnosisEngine
from src.facts import Symptom

engine = MedicalDiagnosisEngine()
engine.reset()

# Add symptoms
engine.declare(Symptom(name='sore_throat', certainty=0.9))
engine.declare(Symptom(name='fever', certainty=0.8))
engine.declare(Symptom(name='swollen_lymph_nodes', certainty=0.7))

# Run inference
engine.run()

# Get results
results = engine.get_diagnosis_results()
for disease, certainty in results:
    print(f"{disease}: {certainty:.2%}")
```

## Medical Accuracy

These rules are based on:

- Common symptom presentations from medical literature
- Typical diagnostic criteria used by healthcare professionals
- Differential diagnosis principles

**Important:** This is an educational tool and should not replace professional medical diagnosis.

## Future Enhancements

Potential improvements:

1. Add age-based rule variations
2. Include severity levels (mild/moderate/severe)
3. Add duration-based rules (acute vs chronic)
4. Implement combination rules for co-infections
5. Add risk factor considerations (smoking, immunocompromised, etc.)
