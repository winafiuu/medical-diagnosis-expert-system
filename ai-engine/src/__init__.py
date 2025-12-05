"""
AI Engine source package.
Contains the core expert system components.
"""

# Import compatibility patch for Python 3.12+ FIRST
from . import compat

from .engine import MedicalDiagnosisEngine
from .facts import Symptom, Diagnosis, Question, PatientInfo

__all__ = ['MedicalDiagnosisEngine', 'Symptom', 'Diagnosis', 'Question', 'PatientInfo']
