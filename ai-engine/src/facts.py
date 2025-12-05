"""
Fact definitions for the medical diagnosis expert system.
This module defines the fact classes used to represent symptoms and diagnoses.
"""

from experta import Fact


class Symptom(Fact):
    """
    Represents a symptom reported by the patient.
    
    Attributes:
        name (str): The name of the symptom (e.g., 'fever', 'cough')
        certainty (float): Certainty factor (0.0 to 1.0) indicating confidence in the symptom
    """
    pass


class Diagnosis(Fact):
    """
    Represents a potential diagnosis.
    
    Attributes:
        disease (str): The name of the disease
        certainty (float): Certainty factor (0.0 to 1.0) indicating confidence in the diagnosis
    """
    pass


class Question(Fact):
    """
    Represents a question that needs to be asked to the user.
    
    Attributes:
        symptom (str): The symptom being inquired about
        text (str): The user-friendly question text
        asked (bool): Whether this question has been asked
    """
    pass


class PatientInfo(Fact):
    """
    Represents general patient information.
    
    Attributes:
        age (int): Patient's age
        gender (str): Patient's gender
        existing_conditions (list): List of pre-existing medical conditions
    """
    pass
