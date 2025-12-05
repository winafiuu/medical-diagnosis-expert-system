"""
Test script for viral disease rules.
This script tests the viral disease diagnostic rules with sample symptom patterns.
"""

import sys
import os

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.engine import MedicalDiagnosisEngine
from src.facts import (
    SYMPTOM_FEVER, SYMPTOM_BODY_ACHES, SYMPTOM_FATIGUE, SYMPTOM_COUGH,
    SYMPTOM_DRY_COUGH, SYMPTOM_LOSS_OF_TASTE, SYMPTOM_LOSS_OF_SMELL,
    SYMPTOM_RUNNY_NOSE, SYMPTOM_SNEEZING, SYMPTOM_SORE_THROAT,
    SYMPTOM_SHORTNESS_OF_BREATH, SYMPTOM_HEADACHE, SYMPTOM_CHILLS
)


def test_influenza():
    """Test classic influenza symptoms."""
    print("\n" + "="*60)
    print("TEST 1: Classic Influenza")
    print("="*60)
    print("Symptoms: High fever, body aches, fatigue, cough")
    
    engine = MedicalDiagnosisEngine()
    engine.reset()
    
    # Add classic flu symptoms
    engine.add_symptom(SYMPTOM_FEVER, 0.9)
    engine.add_symptom(SYMPTOM_BODY_ACHES, 0.8)
    engine.add_symptom(SYMPTOM_FATIGUE, 0.7)
    engine.add_symptom(SYMPTOM_COUGH, 0.6)
    
    # Run the engine
    engine.run()
    
    # Get results
    results = engine.get_diagnosis_results()
    print("\nDiagnosis Results:")
    for disease, certainty in results:
        print(f"  - {disease}: {certainty:.2%} confidence")


def test_covid19():
    """Test classic COVID-19 symptoms."""
    print("\n" + "="*60)
    print("TEST 2: Classic COVID-19")
    print("="*60)
    print("Symptoms: Fever, dry cough, loss of taste/smell, fatigue")
    
    engine = MedicalDiagnosisEngine()
    engine.reset()
    
    # Add classic COVID-19 symptoms
    engine.add_symptom(SYMPTOM_FEVER, 0.8)
    engine.add_symptom(SYMPTOM_DRY_COUGH, 0.7)
    engine.add_symptom(SYMPTOM_LOSS_OF_TASTE, 0.9)
    engine.add_symptom(SYMPTOM_LOSS_OF_SMELL, 0.9)
    engine.add_symptom(SYMPTOM_FATIGUE, 0.6)
    
    # Run the engine
    engine.run()
    
    # Get results
    results = engine.get_diagnosis_results()
    print("\nDiagnosis Results:")
    for disease, certainty in results:
        print(f"  - {disease}: {certainty:.2%} confidence")


def test_common_cold():
    """Test classic common cold symptoms."""
    print("\n" + "="*60)
    print("TEST 3: Classic Common Cold")
    print("="*60)
    print("Symptoms: Runny nose, sneezing, sore throat, mild cough")
    
    engine = MedicalDiagnosisEngine()
    engine.reset()
    
    # Add classic cold symptoms
    engine.add_symptom(SYMPTOM_RUNNY_NOSE, 0.9)
    engine.add_symptom(SYMPTOM_SNEEZING, 0.8)
    engine.add_symptom(SYMPTOM_SORE_THROAT, 0.7)
    engine.add_symptom(SYMPTOM_COUGH, 0.4)
    
    # Run the engine
    engine.run()
    
    # Get results
    results = engine.get_diagnosis_results()
    print("\nDiagnosis Results:")
    for disease, certainty in results:
        print(f"  - {disease}: {certainty:.2%} confidence")


def test_mixed_symptoms():
    """Test with mixed symptoms that could indicate multiple diseases."""
    print("\n" + "="*60)
    print("TEST 4: Mixed Symptoms")
    print("="*60)
    print("Symptoms: Fever, cough, fatigue, runny nose")
    
    engine = MedicalDiagnosisEngine()
    engine.reset()
    
    # Add mixed symptoms
    engine.add_symptom(SYMPTOM_FEVER, 0.6)
    engine.add_symptom(SYMPTOM_COUGH, 0.7)
    engine.add_symptom(SYMPTOM_FATIGUE, 0.5)
    engine.add_symptom(SYMPTOM_RUNNY_NOSE, 0.4)
    
    # Run the engine
    engine.run()
    
    # Get results
    results = engine.get_diagnosis_results()
    print("\nDiagnosis Results:")
    for disease, certainty in results:
        print(f"  - {disease}: {certainty:.2%} confidence")


def test_covid_respiratory():
    """Test COVID-19 with respiratory symptoms."""
    print("\n" + "="*60)
    print("TEST 5: COVID-19 with Respiratory Symptoms")
    print("="*60)
    print("Symptoms: Fever, dry cough, fatigue, shortness of breath")
    
    engine = MedicalDiagnosisEngine()
    engine.reset()
    
    # Add COVID-19 respiratory symptoms
    engine.add_symptom(SYMPTOM_FEVER, 0.8)
    engine.add_symptom(SYMPTOM_DRY_COUGH, 0.8)
    engine.add_symptom(SYMPTOM_FATIGUE, 0.7)
    engine.add_symptom(SYMPTOM_SHORTNESS_OF_BREATH, 0.6)
    
    # Run the engine
    engine.run()
    
    # Get results
    results = engine.get_diagnosis_results()
    print("\nDiagnosis Results:")
    for disease, certainty in results:
        print(f"  - {disease}: {certainty:.2%} confidence")


if __name__ == "__main__":
    print("\n" + "="*60)
    print("VIRAL DISEASE RULES TEST SUITE")
    print("="*60)
    
    try:
        test_influenza()
        test_covid19()
        test_common_cold()
        test_mixed_symptoms()
        test_covid_respiratory()
        
        print("\n" + "="*60)
        print("ALL TESTS COMPLETED SUCCESSFULLY!")
        print("="*60 + "\n")
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
