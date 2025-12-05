"""
Test script for bacterial disease rules.
This script tests the diagnostic rules for Strep Throat, Pneumonia, and Bronchitis.
"""

import sys
import os

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.engine import MedicalDiagnosisEngine
from src.facts import Symptom


def test_strep_throat():
    """Test strep throat diagnosis."""
    print("\n" + "="*60)
    print("TEST 1: Strep Throat - Classic Presentation")
    print("="*60)
    
    engine = MedicalDiagnosisEngine()
    engine.reset()
    
    # Classic strep throat symptoms
    engine.declare(Symptom(name='sore_throat', certainty=0.9))
    engine.declare(Symptom(name='fever', certainty=0.8))
    engine.declare(Symptom(name='swollen_lymph_nodes', certainty=0.7))
    engine.declare(Symptom(name='difficulty_swallowing', certainty=0.8))
    
    engine.run()
    
    results = engine.get_diagnosis_results()
    print("\nSymptoms:")
    print("  - Severe sore throat (90%)")
    print("  - Fever (80%)")
    print("  - Swollen lymph nodes (70%)")
    print("  - Difficulty swallowing (80%)")
    
    print("\nDiagnosis Results:")
    for disease, certainty in results:
        print(f"  - {disease}: {certainty:.2%}")
    
    return results


def test_pneumonia():
    """Test pneumonia diagnosis."""
    print("\n" + "="*60)
    print("TEST 2: Pneumonia - Classic Presentation")
    print("="*60)
    
    engine = MedicalDiagnosisEngine()
    engine.reset()
    
    # Classic pneumonia symptoms
    engine.declare(Symptom(name='fever', certainty=0.9))
    engine.declare(Symptom(name='chest_pain', certainty=0.8))
    engine.declare(Symptom(name='productive_cough', certainty=0.8))
    engine.declare(Symptom(name='shortness_of_breath', certainty=0.7))
    
    engine.run()
    
    results = engine.get_diagnosis_results()
    print("\nSymptoms:")
    print("  - High fever (90%)")
    print("  - Chest pain (80%)")
    print("  - Productive cough (80%)")
    print("  - Shortness of breath (70%)")
    
    print("\nDiagnosis Results:")
    for disease, certainty in results:
        print(f"  - {disease}: {certainty:.2%}")
    
    return results


def test_bronchitis():
    """Test bronchitis diagnosis."""
    print("\n" + "="*60)
    print("TEST 3: Bronchitis - Classic Presentation")
    print("="*60)
    
    engine = MedicalDiagnosisEngine()
    engine.reset()
    
    # Classic bronchitis symptoms
    engine.declare(Symptom(name='cough', certainty=0.9))
    engine.declare(Symptom(name='chest_discomfort', certainty=0.7))
    engine.declare(Symptom(name='mucus_production', certainty=0.8))
    engine.declare(Symptom(name='fatigue', certainty=0.6))
    
    engine.run()
    
    results = engine.get_diagnosis_results()
    print("\nSymptoms:")
    print("  - Persistent cough (90%)")
    print("  - Chest discomfort (70%)")
    print("  - Mucus production (80%)")
    print("  - Fatigue (60%)")
    
    print("\nDiagnosis Results:")
    for disease, certainty in results:
        print(f"  - {disease}: {certainty:.2%}")
    
    return results


def test_mixed_symptoms():
    """Test with mixed symptoms that could indicate multiple conditions."""
    print("\n" + "="*60)
    print("TEST 4: Mixed Symptoms - Pneumonia vs Bronchitis")
    print("="*60)
    
    engine = MedicalDiagnosisEngine()
    engine.reset()
    
    # Symptoms that could indicate either pneumonia or bronchitis
    engine.declare(Symptom(name='productive_cough', certainty=0.8))
    engine.declare(Symptom(name='chest_discomfort', certainty=0.6))
    engine.declare(Symptom(name='fatigue', certainty=0.7))
    engine.declare(Symptom(name='fever', certainty=0.5))
    
    engine.run()
    
    results = engine.get_diagnosis_results()
    print("\nSymptoms:")
    print("  - Productive cough (80%)")
    print("  - Chest discomfort (60%)")
    print("  - Fatigue (70%)")
    print("  - Low-grade fever (50%)")
    
    print("\nDiagnosis Results:")
    for disease, certainty in results:
        print(f"  - {disease}: {certainty:.2%}")
    
    return results


def test_all_diseases():
    """Test with symptoms that could trigger multiple disease rules."""
    print("\n" + "="*60)
    print("TEST 5: Complex Case - Multiple Possible Diagnoses")
    print("="*60)
    
    engine = MedicalDiagnosisEngine()
    engine.reset()
    
    # Complex symptom set
    engine.declare(Symptom(name='fever', certainty=0.7))
    engine.declare(Symptom(name='cough', certainty=0.8))
    engine.declare(Symptom(name='fatigue', certainty=0.7))
    engine.declare(Symptom(name='sore_throat', certainty=0.6))
    engine.declare(Symptom(name='chest_discomfort', certainty=0.5))
    
    engine.run()
    
    results = engine.get_diagnosis_results()
    print("\nSymptoms:")
    print("  - Fever (70%)")
    print("  - Cough (80%)")
    print("  - Fatigue (70%)")
    print("  - Sore throat (60%)")
    print("  - Chest discomfort (50%)")
    
    print("\nDiagnosis Results:")
    for disease, certainty in results:
        print(f"  - {disease}: {certainty:.2%}")
    
    return results


if __name__ == '__main__':
    print("\n" + "="*60)
    print("BACTERIAL DISEASE RULES TEST SUITE")
    print("="*60)
    
    # Run all tests
    test_strep_throat()
    test_pneumonia()
    test_bronchitis()
    test_mixed_symptoms()
    test_all_diseases()
    
    print("\n" + "="*60)
    print("ALL TESTS COMPLETED")
    print("="*60)
    print("\nNote: These are automated tests to verify rule logic.")
    print("Actual medical diagnosis requires professional evaluation.\n")
