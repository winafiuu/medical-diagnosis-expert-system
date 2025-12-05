"""
Fact definitions for the medical diagnosis expert system.
This module defines the fact classes used to represent symptoms and diagnoses.
"""

from experta import Fact


# ============================================================================
# Base Fact Classes
# ============================================================================

class Symptom(Fact):
    """
    Represents a symptom reported by the patient.
    
    Attributes:
        name (str): The name of the symptom (e.g., 'fever', 'cough')
        certainty (float): Certainty factor (0.0 to 1.0) indicating confidence in the symptom
        severity (str): Optional severity level ('mild', 'moderate', 'severe')
    
    Example:
        Symptom(name='fever', certainty=0.9, severity='high')
    """
    pass


class Diagnosis(Fact):
    """
    Represents a potential diagnosis.
    
    Attributes:
        disease (str): The name of the disease
        certainty (float): Certainty factor (0.0 to 1.0) indicating confidence in the diagnosis
        category (str): Disease category ('viral', 'bacterial', 'allergic')
    
    Example:
        Diagnosis(disease='influenza', certainty=0.85, category='viral')
    """
    pass


class Question(Fact):
    """
    Represents a question that needs to be asked to the user.
    
    Attributes:
        symptom (str): The symptom being inquired about
        text (str): The user-friendly question text
        asked (bool): Whether this question has been asked
        priority (int): Priority level for asking (higher = more important)
    
    Example:
        Question(symptom='fever', text='Do you have a fever?', asked=False, priority=10)
    """
    pass


class PatientInfo(Fact):
    """
    Represents general patient information.
    
    Attributes:
        age (int): Patient's age
        gender (str): Patient's gender
        existing_conditions (list): List of pre-existing medical conditions
    
    Example:
        PatientInfo(age=35, gender='male', existing_conditions=['asthma'])
    """
    pass


# ============================================================================
# Specific Symptom Types (for better rule organization)
# ============================================================================

# General Symptoms
SYMPTOM_FEVER = 'fever'
SYMPTOM_FATIGUE = 'fatigue'
SYMPTOM_BODY_ACHES = 'body_aches'
SYMPTOM_HEADACHE = 'headache'
SYMPTOM_CHILLS = 'chills'
SYMPTOM_SWEATING = 'sweating'

# Respiratory Symptoms
SYMPTOM_COUGH = 'cough'
SYMPTOM_DRY_COUGH = 'dry_cough'
SYMPTOM_PRODUCTIVE_COUGH = 'productive_cough'
SYMPTOM_SORE_THROAT = 'sore_throat'
SYMPTOM_RUNNY_NOSE = 'runny_nose'
SYMPTOM_STUFFY_NOSE = 'stuffy_nose'
SYMPTOM_SNEEZING = 'sneezing'
SYMPTOM_SHORTNESS_OF_BREATH = 'shortness_of_breath'
SYMPTOM_CHEST_PAIN = 'chest_pain'
SYMPTOM_CHEST_DISCOMFORT = 'chest_discomfort'
SYMPTOM_WHEEZING = 'wheezing'

# COVID-19 Specific Symptoms
SYMPTOM_LOSS_OF_TASTE = 'loss_of_taste'
SYMPTOM_LOSS_OF_SMELL = 'loss_of_smell'

# Throat/Lymph Symptoms
SYMPTOM_SWOLLEN_LYMPH_NODES = 'swollen_lymph_nodes'
SYMPTOM_DIFFICULTY_SWALLOWING = 'difficulty_swallowing'

# Other Symptoms
SYMPTOM_MUCUS_PRODUCTION = 'mucus_production'
SYMPTOM_NAUSEA = 'nausea'
SYMPTOM_VOMITING = 'vomiting'


# ============================================================================
# Disease Types
# ============================================================================

# Viral Diseases
DISEASE_INFLUENZA = 'influenza'
DISEASE_COVID19 = 'covid-19'
DISEASE_COMMON_COLD = 'common_cold'

# Bacterial Diseases
DISEASE_STREP_THROAT = 'strep_throat'
DISEASE_PNEUMONIA = 'pneumonia'
DISEASE_BRONCHITIS = 'bronchitis'


# ============================================================================
# Certainty Factor Thresholds
# ============================================================================

CF_VERY_HIGH = 0.9  # Very confident (90%+)
CF_HIGH = 0.7       # High confidence (70-89%)
CF_MODERATE = 0.5   # Moderate confidence (50-69%)
CF_LOW = 0.3        # Low confidence (30-49%)
CF_VERY_LOW = 0.1   # Very low confidence (10-29%)


# ============================================================================
# Question Templates
# ============================================================================

QUESTION_TEMPLATES = {
    SYMPTOM_FEVER: "Do you have a fever (elevated body temperature)?",
    SYMPTOM_FATIGUE: "Are you experiencing unusual tiredness or fatigue?",
    SYMPTOM_BODY_ACHES: "Do you have body aches or muscle pain?",
    SYMPTOM_HEADACHE: "Do you have a headache?",
    SYMPTOM_CHILLS: "Are you experiencing chills?",
    SYMPTOM_SWEATING: "Are you experiencing excessive sweating?",
    
    SYMPTOM_COUGH: "Do you have a cough?",
    SYMPTOM_DRY_COUGH: "Is your cough dry (non-productive)?",
    SYMPTOM_PRODUCTIVE_COUGH: "Are you coughing up mucus or phlegm?",
    SYMPTOM_SORE_THROAT: "Do you have a sore throat?",
    SYMPTOM_RUNNY_NOSE: "Do you have a runny nose?",
    SYMPTOM_STUFFY_NOSE: "Is your nose stuffy or congested?",
    SYMPTOM_SNEEZING: "Are you sneezing frequently?",
    SYMPTOM_SHORTNESS_OF_BREATH: "Are you experiencing shortness of breath or difficulty breathing?",
    SYMPTOM_CHEST_PAIN: "Do you have chest pain?",
    SYMPTOM_CHEST_DISCOMFORT: "Do you feel discomfort in your chest?",
    SYMPTOM_WHEEZING: "Are you experiencing wheezing when breathing?",
    
    SYMPTOM_LOSS_OF_TASTE: "Have you lost your sense of taste?",
    SYMPTOM_LOSS_OF_SMELL: "Have you lost your sense of smell?",
    
    SYMPTOM_SWOLLEN_LYMPH_NODES: "Do you have swollen lymph nodes (especially in the neck)?",
    SYMPTOM_DIFFICULTY_SWALLOWING: "Do you have difficulty swallowing?",
    
    SYMPTOM_MUCUS_PRODUCTION: "Are you producing excess mucus?",
    SYMPTOM_NAUSEA: "Are you experiencing nausea?",
    SYMPTOM_VOMITING: "Have you been vomiting?",
}


# ============================================================================
# Disease Information
# ============================================================================

DISEASE_INFO = {
    DISEASE_INFLUENZA: {
        'name': 'Influenza (Flu)',
        'category': 'viral',
        'description': 'A viral infection that attacks the respiratory system',
        'common_symptoms': [SYMPTOM_FEVER, SYMPTOM_BODY_ACHES, SYMPTOM_FATIGUE, SYMPTOM_COUGH, SYMPTOM_HEADACHE]
    },
    DISEASE_COVID19: {
        'name': 'COVID-19',
        'category': 'viral',
        'description': 'A respiratory illness caused by the SARS-CoV-2 virus',
        'common_symptoms': [SYMPTOM_FEVER, SYMPTOM_DRY_COUGH, SYMPTOM_LOSS_OF_TASTE, SYMPTOM_LOSS_OF_SMELL, SYMPTOM_FATIGUE]
    },
    DISEASE_COMMON_COLD: {
        'name': 'Common Cold',
        'category': 'viral',
        'description': 'A viral infection of the upper respiratory tract',
        'common_symptoms': [SYMPTOM_RUNNY_NOSE, SYMPTOM_SNEEZING, SYMPTOM_SORE_THROAT, SYMPTOM_COUGH]
    },
    DISEASE_STREP_THROAT: {
        'name': 'Strep Throat',
        'category': 'bacterial',
        'description': 'A bacterial infection that causes inflammation and pain in the throat',
        'common_symptoms': [SYMPTOM_SORE_THROAT, SYMPTOM_FEVER, SYMPTOM_SWOLLEN_LYMPH_NODES, SYMPTOM_DIFFICULTY_SWALLOWING]
    },
    DISEASE_PNEUMONIA: {
        'name': 'Pneumonia',
        'category': 'bacterial',
        'description': 'An infection that inflames the air sacs in one or both lungs',
        'common_symptoms': [SYMPTOM_FEVER, SYMPTOM_CHEST_PAIN, SYMPTOM_PRODUCTIVE_COUGH, SYMPTOM_SHORTNESS_OF_BREATH]
    },
    DISEASE_BRONCHITIS: {
        'name': 'Bronchitis',
        'category': 'bacterial',
        'description': 'Inflammation of the lining of bronchial tubes',
        'common_symptoms': [SYMPTOM_COUGH, SYMPTOM_CHEST_DISCOMFORT, SYMPTOM_MUCUS_PRODUCTION, SYMPTOM_FATIGUE]
    }
}
