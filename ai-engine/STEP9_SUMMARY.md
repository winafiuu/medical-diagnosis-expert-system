# Step 9: Question-Asking Logic Implementation Summary

## Overview

Successfully implemented goal-driven question generation and dynamic question selection for the medical diagnosis expert system.

## What Was Implemented

### 1. QuestionEngine Class (`src/question_engine.py`)

A sophisticated question-asking engine that implements:

#### Key Features:

- **Symptom Prioritization**: Assigns priority scores (1-10) to symptoms based on diagnostic value

  - High priority (10): Distinctive symptoms like loss of taste/smell (COVID-19 specific)
  - Medium priority (5-7): Common symptoms like fever, cough
  - Lower priority (3-4): Supporting symptoms

- **Information Gain Calculation**: Determines which question would be most informative

  - Combines base symptom priority with discrimination score
  - Favors symptoms that appear in ~50% of diseases (maximum discrimination)
  - Formula: `information_gain = base_priority * (0.7 + 0.3 * discrimination_score)`

- **Dynamic Question Selection**: Chooses next question based on:

  - Current diagnosis certainties
  - Previously asked questions
  - Relevant symptoms for top diagnoses

- **Stopping Criteria**: Determines when to stop asking and provide diagnosis
  - Minimum questions: 5
  - Maximum questions: 15
  - Early stop if high confidence (>80%) reached after minimum questions

### 2. Integration with MedicalDiagnosisEngine

Added new methods to `src/engine.py`:

```python
- get_next_question()        # Get next question based on current state
- get_initial_question()     # Get the first question to start
- record_answer()            # Record user's answer
- should_continue_asking()   # Determine if more questions needed
```

### 3. Updated Main Interface (`main.py`)

Enhanced stdin/stdout interface to:

- Use dynamic question selection instead of hardcoded questions
- Automatically determine when to provide diagnosis vs ask more questions
- Properly track question history

## How It Works

### Question Selection Algorithm:

1. **Identify Relevant Symptoms**: Based on current top diagnoses (certainty > 0.3)
2. **Filter Unasked**: Remove already asked symptoms
3. **Calculate Information Gain**: For each unasked symptom
4. **Select Best**: Choose symptom with highest information gain
5. **Return Question**: Map symptom to user-friendly question text

### Example Flow:

```
1. Start → Ask about fever (common discriminator)
2. User: Yes (0.9) → Multiple diseases possible
3. Ask about loss of smell (high priority, COVID-specific)
4. User: Yes (0.95) → COVID-19 certainty increases
5. Ask about loss of taste (confirms COVID-19)
6. User: Yes (0.95) → High confidence reached
7. Continue until min questions or max confidence
8. Provide diagnosis
```

## Test Results

### Test 1: QuestionEngine Unit Tests ✓

- Initial question generation works
- Question progression follows priority order
- Diagnosis-specific questions are selected correctly

### Test 2: Integrated Engine Tests ✓

- Full diagnosis session completes successfully
- Questions adapt based on previous answers
- COVID-19 correctly diagnosed with 72% certainty after 6 questions

### Test 3: Interactive stdin/stdout Test ✓

- Communication protocol works correctly
- Dynamic question selection functions properly
- Diagnosis provided at appropriate time

## Key Improvements Over Basic Approach

1. **Intelligent Question Selection**: Not just asking random questions, but selecting the most informative ones
2. **Adaptive Behavior**: Questions change based on what we've learned so far
3. **Efficient Diagnosis**: Reaches conclusions faster by asking discriminating questions first
4. **Scalable**: Easy to add new symptoms and diseases without changing the algorithm

## Symptom Priority Rankings

| Priority | Symptoms                                     | Reason                        |
| -------- | -------------------------------------------- | ----------------------------- |
| 10       | loss_of_taste, loss_of_smell                 | Very specific to COVID-19     |
| 9        | chest_pain, shortness_of_breath              | Critical respiratory symptoms |
| 8        | swollen_lymph_nodes, difficulty_swallowing   | Important for strep throat    |
| 7        | fever, dry_cough, productive_cough           | Common but informative        |
| 6        | body_aches, sore_throat                      | Helpful discriminators        |
| 5        | cough, fatigue, runny_nose, sneezing         | Common, less specific         |
| 4        | headache, chest_discomfort, mucus_production | Supporting symptoms           |

## Files Created/Modified

### New Files:

- `ai-engine/src/question_engine.py` - QuestionEngine implementation
- `ai-engine/test_question_logic.py` - Comprehensive test suite
- `ai-engine/test_interactive.py` - Interactive stdin/stdout test

### Modified Files:

- `ai-engine/src/engine.py` - Added QuestionEngine integration
- `ai-engine/main.py` - Updated to use dynamic question selection

## Next Steps (Step 10)

Enhance the stdin/stdout interface with:

- Better error handling for edge cases
- Support for different response formats
- Session management for multiple concurrent diagnoses
