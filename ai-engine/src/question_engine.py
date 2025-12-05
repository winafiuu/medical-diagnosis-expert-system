"""
Question-asking engine for the medical diagnosis expert system.
Implements goal-driven question generation and dynamic question selection.
"""

from typing import List, Dict, Optional, Set, Tuple
from .facts import (
    QUESTION_TEMPLATES, DISEASE_INFO,
    SYMPTOM_FEVER, SYMPTOM_FATIGUE, SYMPTOM_BODY_ACHES, SYMPTOM_HEADACHE,
    SYMPTOM_COUGH, SYMPTOM_DRY_COUGH, SYMPTOM_PRODUCTIVE_COUGH,
    SYMPTOM_SORE_THROAT, SYMPTOM_RUNNY_NOSE, SYMPTOM_SNEEZING,
    SYMPTOM_LOSS_OF_TASTE, SYMPTOM_LOSS_OF_SMELL,
    SYMPTOM_SWOLLEN_LYMPH_NODES, SYMPTOM_DIFFICULTY_SWALLOWING,
    SYMPTOM_CHEST_PAIN, SYMPTOM_SHORTNESS_OF_BREATH,
    SYMPTOM_CHEST_DISCOMFORT, SYMPTOM_MUCUS_PRODUCTION,
    DISEASE_INFLUENZA, DISEASE_COVID19, DISEASE_COMMON_COLD,
    DISEASE_STREP_THROAT, DISEASE_PNEUMONIA, DISEASE_BRONCHITIS
)


class QuestionEngine:
    """
    Manages the question-asking process for the diagnosis system.
    Uses a goal-driven approach to select the most informative questions.
    """
    
    def __init__(self):
        """Initialize the question engine."""
        self.asked_symptoms: Set[str] = set()
        self.answered_symptoms: Dict[str, float] = {}  # symptom -> certainty
        self.symptom_priorities = self._initialize_symptom_priorities()
        
    def reset(self):
        """Reset the question engine for a new session."""
        self.asked_symptoms.clear()
        self.answered_symptoms.clear()
    
    def _initialize_symptom_priorities(self) -> Dict[str, int]:
        """
        Initialize symptom priorities based on their diagnostic value.
        Higher priority = more important for diagnosis.
        
        Returns:
            Dict mapping symptom names to priority values (1-10)
        """
        return {
            # High priority - distinctive symptoms
            SYMPTOM_LOSS_OF_TASTE: 10,  # Very specific to COVID-19
            SYMPTOM_LOSS_OF_SMELL: 10,  # Very specific to COVID-19
            SYMPTOM_CHEST_PAIN: 9,  # Important for pneumonia
            SYMPTOM_SHORTNESS_OF_BREATH: 9,  # Critical respiratory symptom
            SYMPTOM_SWOLLEN_LYMPH_NODES: 8,  # Important for strep throat
            SYMPTOM_DIFFICULTY_SWALLOWING: 8,  # Important for strep throat
            
            # Medium-high priority - common but informative
            SYMPTOM_FEVER: 7,  # Very common, helps narrow down
            SYMPTOM_DRY_COUGH: 7,  # Helps distinguish COVID from others
            SYMPTOM_PRODUCTIVE_COUGH: 7,  # Helps identify bacterial infections
            SYMPTOM_BODY_ACHES: 6,  # Common in flu
            SYMPTOM_SORE_THROAT: 6,  # Important for several conditions
            
            # Medium priority - helpful but less specific
            SYMPTOM_COUGH: 5,  # Very common, less specific
            SYMPTOM_FATIGUE: 5,  # Common in many conditions
            SYMPTOM_RUNNY_NOSE: 5,  # Helps identify cold
            SYMPTOM_SNEEZING: 5,  # Helps identify cold
            SYMPTOM_HEADACHE: 4,  # Common but less specific
            
            # Lower priority - supporting symptoms
            SYMPTOM_CHEST_DISCOMFORT: 4,
            SYMPTOM_MUCUS_PRODUCTION: 4,
        }
    
    def _calculate_information_gain(self, symptom: str, 
                                   current_diagnoses: Dict[str, float]) -> float:
        """
        Calculate the information gain of asking about a symptom.
        This helps determine which question would be most informative.
        
        Args:
            symptom: The symptom to evaluate
            current_diagnoses: Current diagnosis certainties
            
        Returns:
            Information gain score (higher = more informative)
        """
        # Base priority from symptom importance
        base_priority = self.symptom_priorities.get(symptom, 3)
        
        # Count how many diseases are associated with this symptom
        diseases_with_symptom = 0
        for disease, info in DISEASE_INFO.items():
            if symptom in info.get('common_symptoms', []):
                diseases_with_symptom += 1
        
        # Symptoms that appear in some but not all diseases are more informative
        # Ideal is 50% of diseases (maximum discrimination)
        total_diseases = len(DISEASE_INFO)
        discrimination_score = 1.0 - abs(diseases_with_symptom / total_diseases - 0.5) * 2
        
        # Combine base priority with discrimination score
        information_gain = base_priority * (0.7 + 0.3 * discrimination_score)
        
        return information_gain
    
    def _get_relevant_symptoms_for_diagnoses(self, 
                                            diagnoses: Dict[str, float]) -> Set[str]:
        """
        Get symptoms that are relevant to the current top diagnoses.
        
        Args:
            diagnoses: Current diagnosis certainties
            
        Returns:
            Set of relevant symptom names
        """
        relevant_symptoms = set()
        
        # If we have no diagnoses yet, consider all diseases
        if not diagnoses:
            for disease_info in DISEASE_INFO.values():
                relevant_symptoms.update(disease_info.get('common_symptoms', []))
        else:
            # Focus on symptoms for top diagnoses (certainty > 0.3)
            for disease, certainty in diagnoses.items():
                if certainty > 0.3:
                    disease_info = DISEASE_INFO.get(disease, {})
                    relevant_symptoms.update(disease_info.get('common_symptoms', []))
        
        return relevant_symptoms
    
    def get_next_question(self, 
                         current_diagnoses: Dict[str, float]) -> Optional[Dict[str, str]]:
        """
        Determine the next question to ask based on current state.
        
        Args:
            current_diagnoses: Current diagnosis certainties from the engine
            
        Returns:
            Dictionary with 'symptom' and 'text' keys, or None if no more questions
        """
        # Get symptoms relevant to current diagnoses
        relevant_symptoms = self._get_relevant_symptoms_for_diagnoses(current_diagnoses)
        
        # Filter out already asked symptoms
        unasked_symptoms = relevant_symptoms - self.asked_symptoms
        
        # If no relevant symptoms left, ask from remaining high-priority symptoms
        if not unasked_symptoms:
            all_symptoms = set(QUESTION_TEMPLATES.keys())
            unasked_symptoms = all_symptoms - self.asked_symptoms
        
        # If all questions asked, return None
        if not unasked_symptoms:
            return None
        
        # Calculate information gain for each unasked symptom
        symptom_scores: List[Tuple[str, float]] = []
        for symptom in unasked_symptoms:
            score = self._calculate_information_gain(symptom, current_diagnoses)
            symptom_scores.append((symptom, score))
        
        # Sort by score (highest first)
        symptom_scores.sort(key=lambda x: x[1], reverse=True)
        
        # Select the top symptom
        next_symptom = symptom_scores[0][0]
        
        # Get the question text
        question_text = QUESTION_TEMPLATES.get(
            next_symptom, 
            f"Do you have {next_symptom.replace('_', ' ')}?"
        )
        
        return {
            'symptom': next_symptom,
            'text': question_text
        }
    
    def mark_question_asked(self, symptom: str, certainty: float):
        """
        Mark a question as asked and record the answer.
        
        Args:
            symptom: The symptom that was asked about
            certainty: The certainty factor of the answer (0.0 to 1.0)
        """
        self.asked_symptoms.add(symptom)
        self.answered_symptoms[symptom] = certainty
    
    def should_continue_asking(self, 
                              current_diagnoses: Dict[str, float],
                              min_questions: int = 5,
                              max_questions: int = 15) -> bool:
        """
        Determine if we should continue asking questions or provide diagnosis.
        
        Args:
            current_diagnoses: Current diagnosis certainties
            min_questions: Minimum questions to ask before diagnosing
            max_questions: Maximum questions to ask
            
        Returns:
            True if should continue asking, False if ready to diagnose
        """
        questions_asked = len(self.asked_symptoms)
        
        # Always ask at least min_questions
        if questions_asked < min_questions:
            return True
        
        # Stop if we've asked max_questions
        if questions_asked >= max_questions:
            return False
        
        # If we have a high-confidence diagnosis (>0.8), we can stop
        if current_diagnoses:
            max_certainty = max(current_diagnoses.values())
            if max_certainty > 0.8 and questions_asked >= min_questions:
                return False
        
        # If we have no clear diagnosis and haven't hit max, continue
        return True
    
    def get_initial_question(self) -> Dict[str, str]:
        """
        Get the first question to start the diagnosis.
        Usually starts with fever as it's a common discriminating symptom.
        
        Returns:
            Dictionary with 'symptom' and 'text' keys
        """
        # Start with fever as it's a key symptom for many conditions
        return {
            'symptom': SYMPTOM_FEVER,
            'text': QUESTION_TEMPLATES[SYMPTOM_FEVER]
        }
