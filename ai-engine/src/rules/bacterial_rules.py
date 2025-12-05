"""
Bacterial disease diagnostic rules for the medical diagnosis expert system.

This module contains rules for diagnosing bacterial respiratory illnesses:
- Strep Throat
- Pneumonia
- Bronchitis

Each rule includes certainty factors (CF) based on medical literature and 
symptom correlation strength.
"""

from experta import Rule, AND, OR, NOT
from ..facts import (
    Symptom, Diagnosis,
    SYMPTOM_FEVER, SYMPTOM_FATIGUE, SYMPTOM_BODY_ACHES, SYMPTOM_HEADACHE,
    SYMPTOM_COUGH, SYMPTOM_DRY_COUGH, SYMPTOM_PRODUCTIVE_COUGH,
    SYMPTOM_SORE_THROAT, SYMPTOM_RUNNY_NOSE, SYMPTOM_SNEEZING,
    SYMPTOM_SHORTNESS_OF_BREATH, SYMPTOM_CHEST_PAIN, SYMPTOM_CHEST_DISCOMFORT,
    SYMPTOM_SWOLLEN_LYMPH_NODES, SYMPTOM_DIFFICULTY_SWALLOWING,
    SYMPTOM_MUCUS_PRODUCTION, SYMPTOM_WHEEZING,
    DISEASE_STREP_THROAT, DISEASE_PNEUMONIA, DISEASE_BRONCHITIS,
    CF_VERY_HIGH, CF_HIGH, CF_MODERATE
)


# ============================================================================
# Helper method for getting symptom certainty factors
# ============================================================================

def _get_symptom_cf(engine, symptom_name):
    """
    Get the certainty factor for a specific symptom.
    
    Args:
        engine: The engine instance
        symptom_name (str): Name of the symptom
        
    Returns:
        float: Certainty factor (0.0 if symptom not found)
    """
    for fact in engine.facts.values():
        if isinstance(fact, Symptom) and fact.get('name') == symptom_name:
            return fact.get('certainty', 0.0)
    return 0.0


# ============================================================================
# STREP THROAT RULES
# ============================================================================

class StrepThroatRules:
    """Mixin class containing strep throat diagnostic rules."""
    
    @Rule(
        Symptom(name=SYMPTOM_SORE_THROAT),
        Symptom(name=SYMPTOM_FEVER),
        Symptom(name=SYMPTOM_SWOLLEN_LYMPH_NODES),
        Symptom(name=SYMPTOM_DIFFICULTY_SWALLOWING),
        salience=105
    )
    def strep_throat_classic(self):
        """Classic strep throat presentation: Severe sore throat + Fever + Swollen lymph nodes + Difficulty swallowing."""
        throat_cf = _get_symptom_cf(self, SYMPTOM_SORE_THROAT)
        fever_cf = _get_symptom_cf(self, SYMPTOM_FEVER)
        lymph_cf = _get_symptom_cf(self, SYMPTOM_SWOLLEN_LYMPH_NODES)
        swallow_cf = _get_symptom_cf(self, SYMPTOM_DIFFICULTY_SWALLOWING)
        
        # Check for absence of typical cold symptoms
        runny_cf = _get_symptom_cf(self, SYMPTOM_RUNNY_NOSE)
        sneeze_cf = _get_symptom_cf(self, SYMPTOM_SNEEZING)
        
        # Strep throat typically doesn't have runny nose or sneezing
        if (throat_cf >= 0.7 and fever_cf >= 0.6 and lymph_cf >= 0.5 and 
            swallow_cf >= 0.5 and runny_cf < 0.4 and sneeze_cf < 0.4):
            evidence_cf = min(throat_cf, fever_cf, lymph_cf, swallow_cf)
            final_cf = self.apply_rule_confidence(evidence_cf, 0.85)
            self.update_diagnosis(DISEASE_STREP_THROAT, final_cf)
    
    @Rule(
        Symptom(name=SYMPTOM_SORE_THROAT),
        Symptom(name=SYMPTOM_FEVER),
        Symptom(name=SYMPTOM_SWOLLEN_LYMPH_NODES),
        salience=95
    )
    def strep_throat_moderate(self):
        """Moderate strep throat presentation."""
        throat_cf = _get_symptom_cf(self, SYMPTOM_SORE_THROAT)
        fever_cf = _get_symptom_cf(self, SYMPTOM_FEVER)
        lymph_cf = _get_symptom_cf(self, SYMPTOM_SWOLLEN_LYMPH_NODES)
        
        # Check for absence of cough (strep throat typically has no cough)
        cough_cf = _get_symptom_cf(self, SYMPTOM_COUGH)
        
        if throat_cf >= 0.7 and fever_cf >= 0.5 and lymph_cf >= 0.5 and cough_cf < 0.3:
            evidence_cf = min(throat_cf, fever_cf, lymph_cf)
            final_cf = self.apply_rule_confidence(evidence_cf, 0.75)
            self.update_diagnosis(DISEASE_STREP_THROAT, final_cf)
    
    @Rule(
        Symptom(name=SYMPTOM_SORE_THROAT),
        Symptom(name=SYMPTOM_DIFFICULTY_SWALLOWING),
        salience=80
    )
    def strep_throat_mild(self):
        """Mild strep throat presentation with severe throat symptoms."""
        throat_cf = _get_symptom_cf(self, SYMPTOM_SORE_THROAT)
        swallow_cf = _get_symptom_cf(self, SYMPTOM_DIFFICULTY_SWALLOWING)
        
        # Check for absence of typical viral symptoms
        runny_cf = _get_symptom_cf(self, SYMPTOM_RUNNY_NOSE)
        cough_cf = _get_symptom_cf(self, SYMPTOM_COUGH)
        
        if throat_cf >= 0.8 and swallow_cf >= 0.6 and runny_cf < 0.3 and cough_cf < 0.3:
            evidence_cf = min(throat_cf, swallow_cf)
            final_cf = self.apply_rule_confidence(evidence_cf, 0.65)
            self.update_diagnosis(DISEASE_STREP_THROAT, final_cf)


# ============================================================================
# PNEUMONIA RULES
# ============================================================================

class PneumoniaRules:
    """Mixin class containing pneumonia diagnostic rules."""
    
    @Rule(
        Symptom(name=SYMPTOM_FEVER),
        Symptom(name=SYMPTOM_CHEST_PAIN),
        Symptom(name=SYMPTOM_PRODUCTIVE_COUGH),
        Symptom(name=SYMPTOM_SHORTNESS_OF_BREATH),
        salience=115
    )
    def pneumonia_classic(self):
        """Classic pneumonia presentation: High fever + Chest pain + Productive cough + Shortness of breath."""
        fever_cf = _get_symptom_cf(self, SYMPTOM_FEVER)
        chest_cf = _get_symptom_cf(self, SYMPTOM_CHEST_PAIN)
        cough_cf = _get_symptom_cf(self, SYMPTOM_PRODUCTIVE_COUGH)
        breath_cf = _get_symptom_cf(self, SYMPTOM_SHORTNESS_OF_BREATH)
        
        # Pneumonia typically has high fever
        if fever_cf >= 0.7 and chest_cf >= 0.6 and cough_cf >= 0.6 and breath_cf >= 0.5:
            evidence_cf = min(fever_cf, chest_cf, cough_cf, breath_cf)
            final_cf = self.apply_rule_confidence(evidence_cf, 0.90)
            self.update_diagnosis(DISEASE_PNEUMONIA, final_cf)
    
    @Rule(
        Symptom(name=SYMPTOM_FEVER),
        Symptom(name=SYMPTOM_PRODUCTIVE_COUGH),
        Symptom(name=SYMPTOM_SHORTNESS_OF_BREATH),
        salience=100
    )
    def pneumonia_respiratory(self):
        """Pneumonia with prominent respiratory symptoms."""
        fever_cf = _get_symptom_cf(self, SYMPTOM_FEVER)
        cough_cf = _get_symptom_cf(self, SYMPTOM_PRODUCTIVE_COUGH)
        breath_cf = _get_symptom_cf(self, SYMPTOM_SHORTNESS_OF_BREATH)
        
        if fever_cf >= 0.7 and cough_cf >= 0.6 and breath_cf >= 0.6:
            evidence_cf = min(fever_cf, cough_cf, breath_cf)
            final_cf = self.apply_rule_confidence(evidence_cf, 0.80)
            self.update_diagnosis(DISEASE_PNEUMONIA, final_cf)
    
    @Rule(
        Symptom(name=SYMPTOM_CHEST_PAIN),
        Symptom(name=SYMPTOM_PRODUCTIVE_COUGH),
        Symptom(name=SYMPTOM_FEVER),
        salience=90
    )
    def pneumonia_with_chest_pain(self):
        """Pneumonia with significant chest pain."""
        chest_cf = _get_symptom_cf(self, SYMPTOM_CHEST_PAIN)
        cough_cf = _get_symptom_cf(self, SYMPTOM_PRODUCTIVE_COUGH)
        fever_cf = _get_symptom_cf(self, SYMPTOM_FEVER)
        
        if chest_cf >= 0.7 and cough_cf >= 0.5 and fever_cf >= 0.6:
            evidence_cf = min(chest_cf, cough_cf, fever_cf)
            final_cf = self.apply_rule_confidence(evidence_cf, 0.75)
            self.update_diagnosis(DISEASE_PNEUMONIA, final_cf)
    
    @Rule(
        Symptom(name=SYMPTOM_PRODUCTIVE_COUGH),
        Symptom(name=SYMPTOM_SHORTNESS_OF_BREATH),
        Symptom(name=SYMPTOM_FATIGUE),
        salience=85
    )
    def pneumonia_moderate(self):
        """Moderate pneumonia presentation."""
        cough_cf = _get_symptom_cf(self, SYMPTOM_PRODUCTIVE_COUGH)
        breath_cf = _get_symptom_cf(self, SYMPTOM_SHORTNESS_OF_BREATH)
        fatigue_cf = _get_symptom_cf(self, SYMPTOM_FATIGUE)
        
        if cough_cf >= 0.6 and breath_cf >= 0.5 and fatigue_cf >= 0.5:
            evidence_cf = min(cough_cf, breath_cf, fatigue_cf)
            final_cf = self.apply_rule_confidence(evidence_cf, 0.70)
            self.update_diagnosis(DISEASE_PNEUMONIA, final_cf)


# ============================================================================
# BRONCHITIS RULES
# ============================================================================

class BronchitisRules:
    """Mixin class containing bronchitis diagnostic rules."""
    
    @Rule(
        Symptom(name=SYMPTOM_COUGH),
        Symptom(name=SYMPTOM_CHEST_DISCOMFORT),
        Symptom(name=SYMPTOM_MUCUS_PRODUCTION),
        salience=95
    )
    def bronchitis_classic(self):
        """Classic bronchitis presentation: Persistent cough + Chest discomfort + Mucus production."""
        cough_cf = _get_symptom_cf(self, SYMPTOM_COUGH)
        chest_cf = _get_symptom_cf(self, SYMPTOM_CHEST_DISCOMFORT)
        mucus_cf = _get_symptom_cf(self, SYMPTOM_MUCUS_PRODUCTION)
        
        # Check for moderate or no fever (bronchitis typically has low-grade fever or none)
        fever_cf = _get_symptom_cf(self, SYMPTOM_FEVER)
        
        if cough_cf >= 0.7 and chest_cf >= 0.5 and mucus_cf >= 0.6 and fever_cf < 0.7:
            evidence_cf = min(cough_cf, chest_cf, mucus_cf)
            final_cf = self.apply_rule_confidence(evidence_cf, 0.80)
            self.update_diagnosis(DISEASE_BRONCHITIS, final_cf)
    
    @Rule(
        Symptom(name=SYMPTOM_PRODUCTIVE_COUGH),
        Symptom(name=SYMPTOM_CHEST_DISCOMFORT),
        Symptom(name=SYMPTOM_FATIGUE),
        salience=90
    )
    def bronchitis_with_fatigue(self):
        """Bronchitis with productive cough and fatigue."""
        cough_cf = _get_symptom_cf(self, SYMPTOM_PRODUCTIVE_COUGH)
        chest_cf = _get_symptom_cf(self, SYMPTOM_CHEST_DISCOMFORT)
        fatigue_cf = _get_symptom_cf(self, SYMPTOM_FATIGUE)
        
        if cough_cf >= 0.7 and chest_cf >= 0.5 and fatigue_cf >= 0.5:
            evidence_cf = min(cough_cf, chest_cf, fatigue_cf)
            final_cf = self.apply_rule_confidence(evidence_cf, 0.75)
            self.update_diagnosis(DISEASE_BRONCHITIS, final_cf)
    
    @Rule(
        Symptom(name=SYMPTOM_COUGH),
        Symptom(name=SYMPTOM_MUCUS_PRODUCTION),
        salience=80
    )
    def bronchitis_cough_mucus(self):
        """Bronchitis with persistent cough and mucus."""
        cough_cf = _get_symptom_cf(self, SYMPTOM_COUGH)
        mucus_cf = _get_symptom_cf(self, SYMPTOM_MUCUS_PRODUCTION)
        
        # Check for absence of high fever
        fever_cf = _get_symptom_cf(self, SYMPTOM_FEVER)
        
        if cough_cf >= 0.7 and mucus_cf >= 0.6 and fever_cf < 0.7:
            evidence_cf = min(cough_cf, mucus_cf)
            final_cf = self.apply_rule_confidence(evidence_cf, 0.70)
            self.update_diagnosis(DISEASE_BRONCHITIS, final_cf)
    
    @Rule(
        Symptom(name=SYMPTOM_PRODUCTIVE_COUGH),
        Symptom(name=SYMPTOM_WHEEZING),
        salience=85
    )
    def bronchitis_with_wheezing(self):
        """Bronchitis with wheezing."""
        cough_cf = _get_symptom_cf(self, SYMPTOM_PRODUCTIVE_COUGH)
        wheeze_cf = _get_symptom_cf(self, SYMPTOM_WHEEZING)
        
        if cough_cf >= 0.6 and wheeze_cf >= 0.5:
            evidence_cf = min(cough_cf, wheeze_cf)
            final_cf = self.apply_rule_confidence(evidence_cf, 0.70)
            self.update_diagnosis(DISEASE_BRONCHITIS, final_cf)
    
    @Rule(
        Symptom(name=SYMPTOM_COUGH),
        Symptom(name=SYMPTOM_CHEST_DISCOMFORT),
        salience=70
    )
    def bronchitis_mild(self):
        """Mild bronchitis presentation."""
        cough_cf = _get_symptom_cf(self, SYMPTOM_COUGH)
        chest_cf = _get_symptom_cf(self, SYMPTOM_CHEST_DISCOMFORT)
        
        if cough_cf >= 0.7 and chest_cf >= 0.5:
            evidence_cf = min(cough_cf, chest_cf)
            final_cf = self.apply_rule_confidence(evidence_cf, 0.65)
            self.update_diagnosis(DISEASE_BRONCHITIS, final_cf)
