"""
Viral disease diagnostic rules for the medical diagnosis expert system.

This module contains rules for diagnosing viral respiratory illnesses:
- Influenza (Flu)
- COVID-19
- Common Cold

Each rule includes certainty factors (CF) based on medical literature and 
symptom correlation strength.
"""

from experta import Rule, AND, OR, NOT
from ..facts import (
    Symptom, Diagnosis,
    SYMPTOM_FEVER, SYMPTOM_FATIGUE, SYMPTOM_BODY_ACHES, SYMPTOM_HEADACHE,
    SYMPTOM_COUGH, SYMPTOM_DRY_COUGH, SYMPTOM_PRODUCTIVE_COUGH,
    SYMPTOM_SORE_THROAT, SYMPTOM_RUNNY_NOSE, SYMPTOM_SNEEZING,
    SYMPTOM_LOSS_OF_TASTE, SYMPTOM_LOSS_OF_SMELL,
    SYMPTOM_SHORTNESS_OF_BREATH, SYMPTOM_CHEST_PAIN,
    SYMPTOM_STUFFY_NOSE, SYMPTOM_CHILLS,
    DISEASE_INFLUENZA, DISEASE_COVID19, DISEASE_COMMON_COLD,
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
# INFLUENZA (FLU) RULES
# ============================================================================

class InfluenzaRules:
    """Mixin class containing influenza diagnostic rules."""
    
    @Rule(
        Symptom(name=SYMPTOM_FEVER),
        Symptom(name=SYMPTOM_BODY_ACHES),
        Symptom(name=SYMPTOM_FATIGUE),
        Symptom(name=SYMPTOM_COUGH),
        salience=100
    )
    def influenza_classic(self):
        """Classic influenza presentation: High fever + Body aches + Fatigue + Cough."""
        fever_cf = _get_symptom_cf(self, SYMPTOM_FEVER)
        aches_cf = _get_symptom_cf(self, SYMPTOM_BODY_ACHES)
        fatigue_cf = _get_symptom_cf(self, SYMPTOM_FATIGUE)
        cough_cf = _get_symptom_cf(self, SYMPTOM_COUGH)
        
        # Only fire if certainties are high enough
        if fever_cf >= 0.6 and aches_cf >= 0.6 and fatigue_cf >= 0.5 and cough_cf >= 0.4:
            evidence_cf = min(fever_cf, aches_cf, fatigue_cf, cough_cf)
            final_cf = self.apply_rule_confidence(evidence_cf, 0.85)
            self.update_diagnosis(DISEASE_INFLUENZA, final_cf)
    
    @Rule(
        Symptom(name=SYMPTOM_FEVER),
        Symptom(name=SYMPTOM_HEADACHE),
        Symptom(name=SYMPTOM_CHILLS),
        Symptom(name=SYMPTOM_BODY_ACHES),
        salience=90
    )
    def influenza_with_chills(self):
        """Influenza with prominent systemic symptoms."""
        fever_cf = _get_symptom_cf(self, SYMPTOM_FEVER)
        headache_cf = _get_symptom_cf(self, SYMPTOM_HEADACHE)
        chills_cf = _get_symptom_cf(self, SYMPTOM_CHILLS)
        aches_cf = _get_symptom_cf(self, SYMPTOM_BODY_ACHES)
        
        if fever_cf >= 0.6 and headache_cf >= 0.5 and chills_cf >= 0.5 and aches_cf >= 0.5:
            evidence_cf = min(fever_cf, headache_cf, chills_cf, aches_cf)
            final_cf = self.apply_rule_confidence(evidence_cf, 0.75)
            self.update_diagnosis(DISEASE_INFLUENZA, final_cf)
    
    @Rule(
        Symptom(name=SYMPTOM_FEVER),
        Symptom(name=SYMPTOM_FATIGUE),
        Symptom(name=SYMPTOM_COUGH),
        salience=70
    )
    def influenza_moderate(self):
        """Moderate influenza presentation."""
        fever_cf = _get_symptom_cf(self, SYMPTOM_FEVER)
        fatigue_cf = _get_symptom_cf(self, SYMPTOM_FATIGUE)
        cough_cf = _get_symptom_cf(self, SYMPTOM_COUGH)
        
        if fever_cf >= 0.5 and fatigue_cf >= 0.6 and cough_cf >= 0.5:
            evidence_cf = min(fever_cf, fatigue_cf, cough_cf)
            final_cf = self.apply_rule_confidence(evidence_cf, 0.65)
            self.update_diagnosis(DISEASE_INFLUENZA, final_cf)


# ============================================================================
# COVID-19 RULES
# ============================================================================

class Covid19Rules:
    """Mixin class containing COVID-19 diagnostic rules."""
    
    @Rule(
        OR(
            Symptom(name=SYMPTOM_LOSS_OF_TASTE),
            Symptom(name=SYMPTOM_LOSS_OF_SMELL)
        ),
        Symptom(name=SYMPTOM_FEVER),
        Symptom(name=SYMPTOM_DRY_COUGH),
        salience=110
    )
    def covid19_classic(self):
        """Classic COVID-19 with loss of taste/smell."""
        taste_cf = _get_symptom_cf(self, SYMPTOM_LOSS_OF_TASTE)
        smell_cf = _get_symptom_cf(self, SYMPTOM_LOSS_OF_SMELL)
        fever_cf = _get_symptom_cf(self, SYMPTOM_FEVER)
        cough_cf = _get_symptom_cf(self, SYMPTOM_DRY_COUGH)
        
        taste_smell_cf = max(taste_cf, smell_cf)
        if taste_smell_cf >= 0.6 and fever_cf >= 0.5 and cough_cf >= 0.5:
            evidence_cf = min(taste_smell_cf, fever_cf, cough_cf)
            final_cf = self.apply_rule_confidence(evidence_cf, 0.90)
            self.update_diagnosis(DISEASE_COVID19, final_cf)
    
    @Rule(
        Symptom(name=SYMPTOM_FEVER),
        Symptom(name=SYMPTOM_DRY_COUGH),
        Symptom(name=SYMPTOM_FATIGUE),
        Symptom(name=SYMPTOM_SHORTNESS_OF_BREATH),
        salience=95
    )
    def covid19_respiratory(self):
        """COVID-19 with prominent respiratory symptoms."""
        fever_cf = _get_symptom_cf(self, SYMPTOM_FEVER)
        cough_cf = _get_symptom_cf(self, SYMPTOM_DRY_COUGH)
        fatigue_cf = _get_symptom_cf(self, SYMPTOM_FATIGUE)
        breath_cf = _get_symptom_cf(self, SYMPTOM_SHORTNESS_OF_BREATH)
        
        if fever_cf >= 0.6 and cough_cf >= 0.6 and fatigue_cf >= 0.5 and breath_cf >= 0.4:
            evidence_cf = min(fever_cf, cough_cf, fatigue_cf, breath_cf)
            final_cf = self.apply_rule_confidence(evidence_cf, 0.75)
            self.update_diagnosis(DISEASE_COVID19, final_cf)
    
    @Rule(
        Symptom(name=SYMPTOM_FEVER),
        Symptom(name=SYMPTOM_DRY_COUGH),
        Symptom(name=SYMPTOM_FATIGUE),
        salience=75
    )
    def covid19_mild(self):
        """Mild COVID-19 presentation."""
        fever_cf = _get_symptom_cf(self, SYMPTOM_FEVER)
        cough_cf = _get_symptom_cf(self, SYMPTOM_DRY_COUGH)
        fatigue_cf = _get_symptom_cf(self, SYMPTOM_FATIGUE)
        
        if fever_cf >= 0.5 and cough_cf >= 0.5 and fatigue_cf >= 0.5:
            evidence_cf = min(fever_cf, cough_cf, fatigue_cf)
            final_cf = self.apply_rule_confidence(evidence_cf, 0.60)
            self.update_diagnosis(DISEASE_COVID19, final_cf)
    
    @Rule(
        OR(
            Symptom(name=SYMPTOM_LOSS_OF_TASTE),
            Symptom(name=SYMPTOM_LOSS_OF_SMELL)
        ),
        salience=85
    )
    def covid19_taste_smell_only(self):
        """COVID-19 with primarily taste/smell loss."""
        taste_cf = _get_symptom_cf(self, SYMPTOM_LOSS_OF_TASTE)
        smell_cf = _get_symptom_cf(self, SYMPTOM_LOSS_OF_SMELL)
        
        evidence_cf = max(taste_cf, smell_cf)
        if evidence_cf >= 0.7:
            final_cf = self.apply_rule_confidence(evidence_cf, 0.70)
            self.update_diagnosis(DISEASE_COVID19, final_cf)


# ============================================================================
# COMMON COLD RULES
# ============================================================================

class CommonColdRules:
    """Mixin class containing common cold diagnostic rules."""
    
    @Rule(
        Symptom(name=SYMPTOM_RUNNY_NOSE),
        Symptom(name=SYMPTOM_SNEEZING),
        Symptom(name=SYMPTOM_SORE_THROAT),
        salience=90
    )
    def common_cold_classic(self):
        """Classic common cold presentation."""
        runny_cf = _get_symptom_cf(self, SYMPTOM_RUNNY_NOSE)
        sneeze_cf = _get_symptom_cf(self, SYMPTOM_SNEEZING)
        throat_cf = _get_symptom_cf(self, SYMPTOM_SORE_THROAT)
        fever_cf = _get_symptom_cf(self, SYMPTOM_FEVER)
        
        # Check for absence of high fever
        if runny_cf >= 0.6 and sneeze_cf >= 0.5 and throat_cf >= 0.4 and fever_cf < 0.7:
            evidence_cf = min(runny_cf, sneeze_cf, throat_cf)
            final_cf = self.apply_rule_confidence(evidence_cf, 0.80)
            self.update_diagnosis(DISEASE_COMMON_COLD, final_cf)
    
    @Rule(
        OR(
            Symptom(name=SYMPTOM_RUNNY_NOSE),
            Symptom(name=SYMPTOM_STUFFY_NOSE)
        ),
        Symptom(name=SYMPTOM_SNEEZING),
        Symptom(name=SYMPTOM_COUGH),
        salience=85
    )
    def common_cold_nasal(self):
        """Common cold with prominent nasal symptoms."""
        runny_cf = _get_symptom_cf(self, SYMPTOM_RUNNY_NOSE)
        stuffy_cf = _get_symptom_cf(self, SYMPTOM_STUFFY_NOSE)
        sneeze_cf = _get_symptom_cf(self, SYMPTOM_SNEEZING)
        cough_cf = _get_symptom_cf(self, SYMPTOM_COUGH)
        
        nasal_cf = max(runny_cf, stuffy_cf)
        if nasal_cf >= 0.6 and sneeze_cf >= 0.5 and cough_cf >= 0.3:
            evidence_cf = min(nasal_cf, sneeze_cf, cough_cf)
            final_cf = self.apply_rule_confidence(evidence_cf, 0.75)
            self.update_diagnosis(DISEASE_COMMON_COLD, final_cf)
    
    @Rule(
        Symptom(name=SYMPTOM_SORE_THROAT),
        Symptom(name=SYMPTOM_RUNNY_NOSE),
        salience=70
    )
    def common_cold_mild(self):
        """Mild common cold presentation."""
        throat_cf = _get_symptom_cf(self, SYMPTOM_SORE_THROAT)
        runny_cf = _get_symptom_cf(self, SYMPTOM_RUNNY_NOSE)
        
        if throat_cf >= 0.5 and runny_cf >= 0.5:
            evidence_cf = min(throat_cf, runny_cf)
            final_cf = self.apply_rule_confidence(evidence_cf, 0.65)
            self.update_diagnosis(DISEASE_COMMON_COLD, final_cf)
    
    @Rule(
        Symptom(name=SYMPTOM_RUNNY_NOSE),
        Symptom(name=SYMPTOM_COUGH),
        Symptom(name=SYMPTOM_SORE_THROAT),
        salience=75
    )
    def common_cold_with_cough(self):
        """Common cold with cough."""
        runny_cf = _get_symptom_cf(self, SYMPTOM_RUNNY_NOSE)
        cough_cf = _get_symptom_cf(self, SYMPTOM_COUGH)
        throat_cf = _get_symptom_cf(self, SYMPTOM_SORE_THROAT)
        fever_cf = _get_symptom_cf(self, SYMPTOM_FEVER)
        
        if runny_cf >= 0.5 and cough_cf >= 0.5 and throat_cf >= 0.4 and fever_cf < 0.7:
            evidence_cf = min(runny_cf, cough_cf, throat_cf)
            final_cf = self.apply_rule_confidence(evidence_cf, 0.70)
            self.update_diagnosis(DISEASE_COMMON_COLD, final_cf)
