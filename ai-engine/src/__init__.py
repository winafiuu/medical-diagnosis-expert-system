"""
AI Engine source package.
Contains the core expert system components.
"""

from .engine import MedicalDiagnosisEngine
from .facts import Symptom, Diagnosis, Question, PatientInfo

__all__ = ['MedicalDiagnosisEngine', 'Symptom', 'Diagnosis', 'Question', 'PatientInfo']
