"""
Main inference engine for the medical diagnosis expert system.
This module contains the core logic for the expert system using Experta.
"""

# Import compatibility patch for Python 3.12+
from . import compat

from experta import KnowledgeEngine, Rule, AND, OR, NOT
from .facts import Symptom, Diagnosis, Question, PatientInfo
from .rules import InfluenzaRules, Covid19Rules, CommonColdRules


class MedicalDiagnosisEngine(InfluenzaRules, Covid19Rules, CommonColdRules, KnowledgeEngine):
    """
    The main expert system engine for medical diagnosis.
    Uses forward chaining with certainty factors to diagnose respiratory illnesses.
    
    Inherits diagnostic rules from:
    - InfluenzaRules: Rules for diagnosing influenza
    - Covid19Rules: Rules for diagnosing COVID-19
    - CommonColdRules: Rules for diagnosing common cold
    """
    
    def __init__(self):
        super().__init__()
        self.diagnoses = {}  # Store diagnosis results with certainty factors
        self.questions_asked = []  # Track which questions have been asked
        self.next_question = None  # The next question to ask the user
        
    def reset_session(self):
        """Reset the engine for a new diagnosis session."""
        self.reset()
        self.diagnoses = {}
        self.questions_asked = []
        self.next_question = None
    
    def add_symptom(self, symptom_name, certainty):
        """
        Add a symptom to the knowledge base.
        
        Args:
            symptom_name (str): Name of the symptom
            certainty (float): Certainty factor (0.0 to 1.0)
        """
        self.declare(Symptom(name=symptom_name, certainty=certainty))
    
    def get_diagnosis_results(self):
        """
        Get the current diagnosis results sorted by certainty.
        
        Returns:
            list: List of tuples (disease_name, certainty_factor) sorted by certainty
        """
        return sorted(self.diagnoses.items(), key=lambda x: x[1], reverse=True)
    
    def combine_certainty_and(self, cf1, cf2):
        """
        Combine certainty factors using AND logic (minimum).
        
        Args:
            cf1 (float): First certainty factor
            cf2 (float): Second certainty factor
            
        Returns:
            float: Combined certainty factor
        """
        return min(cf1, cf2)
    
    def combine_certainty_or(self, cf1, cf2):
        """
        Combine certainty factors using OR logic (maximum).
        
        Args:
            cf1 (float): First certainty factor
            cf2 (float): Second certainty factor
            
        Returns:
            float: Combined certainty factor
        """
        return max(cf1, cf2)
    
    def apply_rule_confidence(self, evidence_cf, rule_cf):
        """
        Apply rule confidence to evidence certainty.
        
        Args:
            evidence_cf (float): Certainty factor from evidence
            rule_cf (float): Reliability of the rule itself
            
        Returns:
            float: Final certainty factor
        """
        return evidence_cf * rule_cf
    
    def update_diagnosis(self, disease, certainty):
        """
        Update or add a diagnosis with the given certainty.
        If the disease already exists, combine certainties.
        
        Args:
            disease (str): Name of the disease
            certainty (float): Certainty factor for this diagnosis
        """
        if disease in self.diagnoses:
            # Combine with existing certainty using OR logic
            self.diagnoses[disease] = self.combine_certainty_or(
                self.diagnoses[disease], 
                certainty
            )
        else:
            self.diagnoses[disease] = certainty


