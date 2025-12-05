#!/usr/bin/env python3
"""
Visual demonstration of the question-asking logic.
Shows how questions are selected dynamically based on symptoms.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.engine import MedicalDiagnosisEngine
from src.facts import DISEASE_INFO


def print_header(text):
    """Print a formatted header."""
    print("\n" + "=" * 70)
    print(f"  {text}")
    print("=" * 70)


def print_diagnoses(engine, title="Current Diagnoses"):
    """Print current diagnosis state."""
    results = engine.get_diagnosis_results()
    if results:
        print(f"\n{title}:")
        for disease, certainty in results[:3]:
            disease_name = DISEASE_INFO.get(disease, {}).get('name', disease)
            bar_length = int(certainty * 40)
            bar = "█" * bar_length + "░" * (40 - bar_length)
            print(f"  {disease_name:<20} [{bar}] {certainty:.1%}")
    else:
        print(f"\n{title}: None yet")


def simulate_scenario(name, symptoms):
    """Simulate a diagnosis scenario."""
    print_header(f"Scenario: {name}")
    
    engine = MedicalDiagnosisEngine()
    engine.reset_session()
    
    # Get initial question
    question = engine.get_initial_question()
    print(f"\n🤖 AI: {question['text']}")
    
    for i, (symptom, certainty, user_response) in enumerate(symptoms, 1):
        print(f"👤 User: {user_response}")
        
        # Record answer and add symptom
        engine.record_answer(symptom, certainty)
        engine.add_symptom(symptom, certainty)
        engine.run()
        
        # Show current diagnoses
        print_diagnoses(engine, f"After Question {i}")
        
        # Check if should continue
        if not engine.should_continue_asking():
            print("\n✓ Sufficient information gathered!")
            break
        
        # Get next question
        next_q = engine.get_next_question()
        if next_q:
            print(f"\n🤖 AI: {next_q['text']}")
        else:
            print("\n✓ No more questions available!")
            break
    
    # Final diagnosis
    print_diagnoses(engine, "Final Diagnosis")
    print(f"\nTotal questions asked: {len(engine.questions_asked)}")


def main():
    """Run multiple scenario demonstrations."""
    print_header("QUESTION-ASKING LOGIC DEMONSTRATION")
    
    # Scenario 1: COVID-19 case
    simulate_scenario(
        "COVID-19 Patient",
        [
            ('fever', 0.9, "Yes, I have a high fever (39°C)"),
            ('loss_of_smell', 0.95, "Yes, I completely lost my sense of smell"),
            ('loss_of_taste', 0.95, "Yes, I can't taste anything"),
            ('dry_cough', 0.8, "Yes, persistent dry cough"),
            ('fatigue', 0.7, "Yes, feeling very tired"),
        ]
    )
    
    # Scenario 2: Common Cold case
    simulate_scenario(
        "Common Cold Patient",
        [
            ('fever', 0.3, "Maybe a slight fever, not sure"),
            ('runny_nose', 0.9, "Yes, very runny nose"),
            ('sneezing', 0.9, "Yes, sneezing a lot"),
            ('sore_throat', 0.6, "Yes, mild sore throat"),
            ('cough', 0.5, "A little cough, not too bad"),
        ]
    )
    
    # Scenario 3: Pneumonia case
    simulate_scenario(
        "Pneumonia Patient",
        [
            ('fever', 0.95, "Yes, very high fever (40°C)"),
            ('chest_pain', 0.9, "Yes, severe chest pain when breathing"),
            ('productive_cough', 0.85, "Yes, coughing up yellow mucus"),
            ('shortness_of_breath', 0.8, "Yes, difficulty breathing"),
            ('fatigue', 0.7, "Yes, very weak and tired"),
        ]
    )
    
    print_header("DEMONSTRATION COMPLETE")
    print("\nKey Observations:")
    print("  • Questions adapt based on previous answers")
    print("  • High-priority symptoms (loss of taste/smell) asked early")
    print("  • System reaches diagnosis efficiently")
    print("  • Different symptom patterns lead to different diagnoses")
    print()


if __name__ == '__main__':
    main()
