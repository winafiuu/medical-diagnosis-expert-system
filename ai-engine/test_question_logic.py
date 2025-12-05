#!/usr/bin/env python3
"""
Test script for the question-asking logic.
Tests the QuestionEngine and its integration with the MedicalDiagnosisEngine.
"""

import sys
import os

# Add the parent directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.engine import MedicalDiagnosisEngine
from src.question_engine import QuestionEngine
from src.facts import DISEASE_INFO


def test_question_engine():
    """Test the QuestionEngine independently."""
    print("=" * 70)
    print("Testing QuestionEngine")
    print("=" * 70)
    
    qe = QuestionEngine()
    
    # Test 1: Get initial question
    print("\n1. Testing initial question:")
    initial_q = qe.get_initial_question()
    print(f"   Initial question: {initial_q}")
    
    # Test 2: Get next question with no diagnoses
    print("\n2. Testing next question with no diagnoses:")
    next_q = qe.get_next_question({})
    print(f"   Next question: {next_q}")
    
    # Test 3: Mark questions as asked and get new ones
    print("\n3. Testing question progression:")
    for i in range(5):
        if next_q:
            symptom = next_q['symptom']
            qe.mark_question_asked(symptom, 0.8)
            print(f"   Asked: {symptom}")
            next_q = qe.get_next_question({})
    
    # Test 4: Test with specific diagnoses
    print("\n4. Testing with COVID-19 diagnosis:")
    qe.reset()
    diagnoses = {'covid-19': 0.7}
    next_q = qe.get_next_question(diagnoses)
    print(f"   Next question for COVID-19: {next_q}")
    
    print("\n✓ QuestionEngine tests completed\n")


def test_integrated_engine():
    """Test the integrated MedicalDiagnosisEngine with question-asking."""
    print("=" * 70)
    print("Testing Integrated MedicalDiagnosisEngine")
    print("=" * 70)
    
    engine = MedicalDiagnosisEngine()
    
    # Test 1: Start session and get initial question
    print("\n1. Starting new session:")
    engine.reset_session()
    initial_q = engine.get_initial_question()
    print(f"   Initial question: {initial_q}")
    
    # Test 2: Simulate answering questions
    print("\n2. Simulating diagnosis session:")
    
    # Answer: Yes to fever (high certainty)
    print("\n   Q: Do you have a fever?")
    print("   A: Yes (certainty: 0.9)")
    engine.record_answer('fever', 0.9)
    engine.add_symptom('fever', 0.9)
    engine.run()
    
    next_q = engine.get_next_question()
    print(f"   Next question: {next_q}")
    
    # Answer: Yes to dry cough
    print("\n   Q: Do you have a dry cough?")
    print("   A: Yes (certainty: 0.8)")
    engine.record_answer('dry_cough', 0.8)
    engine.add_symptom('dry_cough', 0.8)
    engine.run()
    
    next_q = engine.get_next_question()
    print(f"   Next question: {next_q}")
    
    # Answer: Yes to loss of taste
    print("\n   Q: Have you lost your sense of taste?")
    print("   A: Yes (certainty: 0.9)")
    engine.record_answer('loss_of_taste', 0.9)
    engine.add_symptom('loss_of_taste', 0.9)
    engine.run()
    
    # Test 3: Check current diagnoses
    print("\n3. Current diagnoses after 3 symptoms:")
    results = engine.get_diagnosis_results()
    for disease, certainty in results[:3]:
        disease_name = DISEASE_INFO.get(disease, {}).get('name', disease)
        print(f"   - {disease_name}: {certainty:.2%}")
    
    # Test 4: Check if should continue asking
    print("\n4. Should continue asking questions?")
    should_continue = engine.should_continue_asking()
    print(f"   {should_continue}")
    
    # Continue asking a few more questions
    print("\n5. Continuing with more questions:")
    for i in range(3):
        if should_continue:
            next_q = engine.get_next_question()
            if next_q:
                symptom = next_q['symptom']
                print(f"\n   Q: {next_q['text']}")
                # Simulate random answer
                certainty = 0.5
                print(f"   A: Maybe (certainty: {certainty})")
                engine.record_answer(symptom, certainty)
                engine.add_symptom(symptom, certainty)
                engine.run()
                should_continue = engine.should_continue_asking()
    
    # Test 5: Final diagnosis
    print("\n6. Final diagnosis:")
    results = engine.get_diagnosis_results()
    print(f"   Total questions asked: {len(engine.questions_asked)}")
    print(f"   Top 3 diagnoses:")
    for disease, certainty in results[:3]:
        disease_name = DISEASE_INFO.get(disease, {}).get('name', disease)
        print(f"   - {disease_name}: {certainty:.2%}")
    
    print("\n✓ Integrated engine tests completed\n")


def test_information_gain():
    """Test the information gain calculation."""
    print("=" * 70)
    print("Testing Information Gain Calculation")
    print("=" * 70)
    
    qe = QuestionEngine()
    
    print("\nSymptom priorities and information gain:")
    print(f"{'Symptom':<30} {'Priority':<10} {'Info Gain':<10}")
    print("-" * 50)
    
    # Test with no current diagnoses
    test_symptoms = [
        'fever', 'loss_of_taste', 'loss_of_smell', 'chest_pain',
        'cough', 'sore_throat', 'runny_nose'
    ]
    
    for symptom in test_symptoms:
        priority = qe.symptom_priorities.get(symptom, 3)
        info_gain = qe._calculate_information_gain(symptom, {})
        print(f"{symptom:<30} {priority:<10} {info_gain:<10.2f}")
    
    print("\n✓ Information gain tests completed\n")


if __name__ == '__main__':
    print("\n" + "=" * 70)
    print("QUESTION-ASKING LOGIC TEST SUITE")
    print("=" * 70 + "\n")
    
    try:
        test_question_engine()
        test_integrated_engine()
        test_information_gain()
        
        print("=" * 70)
        print("✓ ALL TESTS PASSED")
        print("=" * 70 + "\n")
        
    except Exception as e:
        print(f"\n✗ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
