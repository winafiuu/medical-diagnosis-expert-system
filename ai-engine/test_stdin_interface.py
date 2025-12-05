#!/usr/bin/env python3
"""
Test script for the stdin/stdout interface.
This simulates how the Node.js backend will communicate with the Python engine.
"""

import subprocess
import json
import sys

def test_stdin_interface():
    """Test the stdin/stdout interface of main.py"""
    
    print("🧪 Testing AI Engine stdin/stdout Interface\n")
    print("=" * 60)
    
    # Start the Python process
    process = subprocess.Popen(
        ['python3', 'main.py'],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1
    )
    
    try:
        # Test 1: Start a new diagnosis session
        print("\n📝 Test 1: Starting diagnosis session...")
        start_command = json.dumps({"action": "start"}) + "\n"
        process.stdin.write(start_command)
        process.stdin.flush()
        
        response = process.stdout.readline()
        result = json.loads(response)
        print(f"✅ Response: {json.dumps(result, indent=2)}")
        
        # Test 2: Add a symptom (fever with high certainty)
        print("\n📝 Test 2: Adding symptom 'fever' with certainty 0.9...")
        add_symptom_command = json.dumps({
            "action": "add_symptom",
            "symptom": "fever",
            "certainty": 0.9
        }) + "\n"
        process.stdin.write(add_symptom_command)
        process.stdin.flush()
        
        response = process.stdout.readline()
        result = json.loads(response)
        print(f"✅ Response: {json.dumps(result, indent=2)}")
        
        # Test 3: Add another symptom (cough)
        print("\n📝 Test 3: Adding symptom 'cough' with certainty 0.8...")
        add_symptom_command = json.dumps({
            "action": "add_symptom",
            "symptom": "cough",
            "certainty": 0.8
        }) + "\n"
        process.stdin.write(add_symptom_command)
        process.stdin.flush()
        
        response = process.stdout.readline()
        result = json.loads(response)
        print(f"✅ Response: {json.dumps(result, indent=2)}")
        
        # Test 4: Add body aches
        print("\n📝 Test 4: Adding symptom 'body_aches' with certainty 0.85...")
        add_symptom_command = json.dumps({
            "action": "add_symptom",
            "symptom": "body_aches",
            "certainty": 0.85
        }) + "\n"
        process.stdin.write(add_symptom_command)
        process.stdin.flush()
        
        response = process.stdout.readline()
        result = json.loads(response)
        print(f"✅ Response: {json.dumps(result, indent=2)}")
        
        # Test 5: Invalid JSON
        print("\n📝 Test 5: Testing error handling with invalid JSON...")
        invalid_command = "this is not json\n"
        process.stdin.write(invalid_command)
        process.stdin.flush()
        
        response = process.stdout.readline()
        result = json.loads(response)
        print(f"✅ Response: {json.dumps(result, indent=2)}")
        
        # Test 6: Invalid action
        print("\n📝 Test 6: Testing error handling with invalid action...")
        invalid_action = json.dumps({"action": "invalid_action"}) + "\n"
        process.stdin.write(invalid_action)
        process.stdin.flush()
        
        response = process.stdout.readline()
        result = json.loads(response)
        print(f"✅ Response: {json.dumps(result, indent=2)}")
        
        # Test 7: Missing symptom parameter
        print("\n📝 Test 7: Testing error handling with missing symptom...")
        missing_symptom = json.dumps({
            "action": "add_symptom",
            "certainty": 0.8
        }) + "\n"
        process.stdin.write(missing_symptom)
        process.stdin.flush()
        
        response = process.stdout.readline()
        result = json.loads(response)
        print(f"✅ Response: {json.dumps(result, indent=2)}")
        
        print("\n" + "=" * 60)
        print("✅ All tests completed successfully!")
        
    except Exception as e:
        print(f"\n❌ Error during testing: {e}")
        stderr = process.stderr.read()
        if stderr:
            print(f"stderr: {stderr}")
    
    finally:
        # Clean up
        process.stdin.close()
        process.terminate()
        process.wait()

if __name__ == '__main__':
    test_stdin_interface()
