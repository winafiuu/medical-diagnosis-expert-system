"""
Main entry point for the AI diagnosis engine.
Provides a stdin/stdout interface for communication with the Node.js backend.
"""

import sys
import json
from src.engine import MedicalDiagnosisEngine


def main():
    """
    Main function that handles stdin/stdout communication.
    
    Expected input format (JSON):
    {
        "action": "start" | "add_symptom" | "get_diagnosis",
        "symptom": "symptom_name",  // for add_symptom action
        "certainty": 0.8  // for add_symptom action (0.0 to 1.0)
    }
    
    Output format (JSON):
    {
        "status": "success" | "error",
        "next_question": {
            "symptom": "fever",
            "text": "Do you have a fever?"
        },  // if more questions needed
        "diagnosis": [
            {"disease": "Influenza", "certainty": 0.85},
            {"disease": "COVID-19", "certainty": 0.65}
        ],  // if diagnosis complete
        "message": "Error message"  // if error
    }
    """
    
    engine = MedicalDiagnosisEngine()
    
    try:
        # Read from stdin
        for line in sys.stdin:
            try:
                data = json.loads(line.strip())
                action = data.get('action')
                
                if action == 'start':
                    # Start a new diagnosis session
                    engine.reset_session()
                    
                    # Get the initial question
                    initial_question = engine.get_initial_question()
                    
                    response = {
                        'status': 'success',
                        'message': 'Diagnosis session started',
                        'next_question': initial_question
                    }
                
                elif action == 'add_symptom':
                    # Add a symptom to the knowledge base
                    symptom = data.get('symptom')
                    certainty = data.get('certainty', 1.0)
                    
                    if not symptom:
                        response = {
                            'status': 'error',
                            'message': 'Symptom name is required'
                        }
                    else:
                        # Record the answer
                        engine.record_answer(symptom, certainty)
                        
                        # Add symptom to knowledge base
                        engine.add_symptom(symptom, certainty)
                        
                        # Run the inference engine
                        engine.run()
                        
                        # Check if we should continue asking or provide diagnosis
                        if engine.should_continue_asking():
                            # Get next question
                            next_question = engine.get_next_question()
                            
                            if next_question:
                                response = {
                                    'status': 'success',
                                    'message': 'Symptom recorded',
                                    'next_question': next_question
                                }
                            else:
                                # No more questions, provide diagnosis
                                results = engine.get_diagnosis_results()
                                diagnosis_list = [
                                    {'disease': disease, 'certainty': certainty}
                                    for disease, certainty in results
                                ]
                                response = {
                                    'status': 'success',
                                    'diagnosis': diagnosis_list
                                }
                        else:
                            # Ready to provide diagnosis
                            results = engine.get_diagnosis_results()
                            diagnosis_list = [
                                {'disease': disease, 'certainty': certainty}
                                for disease, certainty in results
                            ]
                            response = {
                                'status': 'success',
                                'diagnosis': diagnosis_list
                            }
                
                elif action == 'get_diagnosis':
                    # Get the final diagnosis
                    engine.run()  # Ensure all rules are fired
                    results = engine.get_diagnosis_results()
                    
                    diagnosis_list = [
                        {'disease': disease, 'certainty': certainty}
                        for disease, certainty in results
                    ]
                    
                    response = {
                        'status': 'success',
                        'diagnosis': diagnosis_list
                    }
                
                else:
                    response = {
                        'status': 'error',
                        'message': f'Unknown action: {action}'
                    }
                
                # Write response to stdout
                print(json.dumps(response), flush=True)
                
            except json.JSONDecodeError as e:
                error_response = {
                    'status': 'error',
                    'message': f'Invalid JSON input: {str(e)}'
                }
                print(json.dumps(error_response), flush=True)
            
            except Exception as e:
                error_response = {
                    'status': 'error',
                    'message': f'Internal error: {str(e)}'
                }
                print(json.dumps(error_response), flush=True)
    
    except KeyboardInterrupt:
        # Graceful shutdown
        pass


if __name__ == '__main__':
    main()

