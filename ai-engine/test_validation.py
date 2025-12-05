#!/usr/bin/env python3
"""
Validation test script for the stdin/stdout interface.
Tests all input validation rules and error handling.
"""

import subprocess
import json
import sys

def send_command(process, command):
    """Send a command and get the response"""
    process.stdin.write(json.dumps(command) + "\n")
    process.stdin.flush()
    response = process.stdout.readline()
    return json.loads(response)

def test_validation():
    """Test all validation rules"""
    
    print("🧪 Testing Input Validation\n")
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
        # Test 1: Valid certainty at lower boundary (0.0)
        print("\n📝 Test 1: Certainty = 0.0 (valid lower boundary)...")
        result = send_command(process, {
            "action": "start"
        })
        result = send_command(process, {
            "action": "add_symptom",
            "symptom": "fever",
            "certainty": 0.0
        })
        assert result['status'] == 'success', f"Expected success, got {result}"
        print(f"✅ PASS: {result['status']}")
        
        # Test 2: Valid certainty at upper boundary (1.0)
        print("\n📝 Test 2: Certainty = 1.0 (valid upper boundary)...")
        result = send_command(process, {
            "action": "add_symptom",
            "symptom": "cough",
            "certainty": 1.0
        })
        assert result['status'] == 'success', f"Expected success, got {result}"
        print(f"✅ PASS: {result['status']}")
        
        # Test 3: Invalid certainty below range
        print("\n📝 Test 3: Certainty = -0.1 (invalid - below range)...")
        result = send_command(process, {
            "action": "add_symptom",
            "symptom": "fatigue",
            "certainty": -0.1
        })
        assert result['status'] == 'error', f"Expected error, got {result}"
        assert result['error_code'] == 'CERTAINTY_OUT_OF_RANGE', f"Expected CERTAINTY_OUT_OF_RANGE, got {result.get('error_code')}"
        print(f"✅ PASS: {result['error_code']} - {result['message']}")
        
        # Test 4: Invalid certainty above range
        print("\n📝 Test 4: Certainty = 1.5 (invalid - above range)...")
        result = send_command(process, {
            "action": "add_symptom",
            "symptom": "headache",
            "certainty": 1.5
        })
        assert result['status'] == 'error', f"Expected error, got {result}"
        assert result['error_code'] == 'CERTAINTY_OUT_OF_RANGE', f"Expected CERTAINTY_OUT_OF_RANGE, got {result.get('error_code')}"
        print(f"✅ PASS: {result['error_code']} - {result['message']}")
        
        # Test 5: Invalid certainty type (string)
        print("\n📝 Test 5: Certainty = 'high' (invalid - wrong type)...")
        result = send_command(process, {
            "action": "add_symptom",
            "symptom": "sore_throat",
            "certainty": "high"
        })
        assert result['status'] == 'error', f"Expected error, got {result}"
        assert result['error_code'] == 'INVALID_CERTAINTY_TYPE', f"Expected INVALID_CERTAINTY_TYPE, got {result.get('error_code')}"
        print(f"✅ PASS: {result['error_code']} - {result['message']}")
        
        # Test 6: Missing symptom parameter
        print("\n📝 Test 6: Missing symptom parameter...")
        result = send_command(process, {
            "action": "add_symptom",
            "certainty": 0.8
        })
        assert result['status'] == 'error', f"Expected error, got {result}"
        assert result['error_code'] == 'MISSING_SYMPTOM', f"Expected MISSING_SYMPTOM, got {result.get('error_code')}"
        print(f"✅ PASS: {result['error_code']} - {result['message']}")
        
        # Test 7: Invalid action
        print("\n📝 Test 7: Invalid action...")
        result = send_command(process, {
            "action": "delete_symptom"
        })
        assert result['status'] == 'error', f"Expected error, got {result}"
        assert result['error_code'] == 'INVALID_ACTION', f"Expected INVALID_ACTION, got {result.get('error_code')}"
        print(f"✅ PASS: {result['error_code']} - {result['message']}")
        
        # Test 8: Invalid JSON
        print("\n📝 Test 8: Invalid JSON...")
        process.stdin.write("not valid json\n")
        process.stdin.flush()
        response = process.stdout.readline()
        result = json.loads(response)
        assert result['status'] == 'error', f"Expected error, got {result}"
        assert result['error_code'] == 'INVALID_JSON', f"Expected INVALID_JSON, got {result.get('error_code')}"
        print(f"✅ PASS: {result['error_code']} - {result['message']}")
        
        # Test 9: Valid integer certainty (should be accepted)
        print("\n📝 Test 9: Certainty = 1 (integer, should be accepted)...")
        result = send_command(process, {
            "action": "start"
        })
        result = send_command(process, {
            "action": "add_symptom",
            "symptom": "runny_nose",
            "certainty": 1
        })
        assert result['status'] == 'success', f"Expected success, got {result}"
        print(f"✅ PASS: {result['status']}")
        
        # Test 10: Default certainty (when not provided)
        print("\n📝 Test 10: No certainty provided (should default to 1.0)...")
        result = send_command(process, {
            "action": "add_symptom",
            "symptom": "sneezing"
        })
        assert result['status'] == 'success', f"Expected success, got {result}"
        print(f"✅ PASS: {result['status']} (defaulted to 1.0)")
        
        print("\n" + "=" * 60)
        print("✅ All validation tests passed!")
        
    except AssertionError as e:
        print(f"\n❌ Test failed: {e}")
        return False
    except Exception as e:
        print(f"\n❌ Error during testing: {e}")
        stderr = process.stderr.read()
        if stderr:
            print(f"stderr: {stderr}")
        return False
    finally:
        # Clean up
        process.stdin.close()
        process.terminate()
        process.wait()
    
    return True

if __name__ == '__main__':
    success = test_validation()
    sys.exit(0 if success else 1)
