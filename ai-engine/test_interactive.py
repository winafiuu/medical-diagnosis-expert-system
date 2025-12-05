#!/usr/bin/env python3
"""
Interactive test for the stdin/stdout interface with question-asking logic.
This simulates how the Node.js backend will interact with the Python AI engine.
"""

import json
import subprocess
import sys


def send_command(process, command):
    """Send a command to the process and get the response."""
    command_json = json.dumps(command) + '\n'
    process.stdin.write(command_json)
    process.stdin.flush()
    
    response_line = process.stdout.readline()
    return json.loads(response_line)


def main():
    """Run an interactive diagnosis session."""
    print("=" * 70)
    print("INTERACTIVE DIAGNOSIS SESSION TEST")
    print("=" * 70)
    
    # Start the Python process
    process = subprocess.Popen(
        ['python', 'main.py'],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1
    )
    
    try:
        # Test 1: Start a new session
        print("\n1. Starting diagnosis session...")
        response = send_command(process, {'action': 'start'})
        print(f"   Status: {response['status']}")
        print(f"   Message: {response.get('message', '')}")
        
        if 'next_question' in response:
            print(f"   First Question: {response['next_question']['text']}")
        
        # Test 2: Simulate a COVID-19 case
        print("\n2. Simulating COVID-19 symptoms...")
        
        symptoms_to_add = [
            ('fever', 0.9, 'Yes, high fever'),
            ('dry_cough', 0.8, 'Yes, persistent dry cough'),
            ('loss_of_taste', 0.95, 'Yes, complete loss of taste'),
            ('loss_of_smell', 0.95, 'Yes, cannot smell anything'),
            ('fatigue', 0.7, 'Yes, feeling very tired'),
        ]
        
        for symptom, certainty, answer in symptoms_to_add:
            print(f"\n   Adding symptom: {symptom} (certainty: {certainty})")
            print(f"   User answer: {answer}")
            
            response = send_command(process, {
                'action': 'add_symptom',
                'symptom': symptom,
                'certainty': certainty
            })
            
            print(f"   Status: {response['status']}")
            
            if 'next_question' in response:
                print(f"   Next Question: {response['next_question']['text']}")
            
            if 'diagnosis' in response:
                print("\n   ✓ Diagnosis ready!")
                print("   Top diagnoses:")
                for diag in response['diagnosis'][:3]:
                    print(f"      - {diag['disease']}: {diag['certainty']:.2%}")
                break
        
        # Test 3: Get final diagnosis if not already provided
        if 'diagnosis' not in response:
            print("\n3. Getting final diagnosis...")
            response = send_command(process, {'action': 'get_diagnosis'})
            
            if response['status'] == 'success' and 'diagnosis' in response:
                print("   Final diagnosis:")
                for diag in response['diagnosis'][:5]:
                    print(f"      - {diag['disease']}: {diag['certainty']:.2%}")
        
        print("\n" + "=" * 70)
        print("✓ INTERACTIVE TEST COMPLETED SUCCESSFULLY")
        print("=" * 70)
        
    except Exception as e:
        print(f"\n✗ Error during test: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    finally:
        # Clean up
        process.terminate()
        process.wait()
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
