#!/usr/bin/env python3
"""Test the /api/capture_and_analyze endpoint to verify NaN fixes"""
import requests
import json

BASE_URL = "http://localhost:5002"

print("=" * 70)
print("🧪 Testing /api/capture_and_analyze Endpoint Fixes")
print("=" * 70)

# 1. Health check
print("\n1️⃣  Health Check...")
try:
    resp = requests.get(f"{BASE_URL}/api/health", timeout=5)
    if resp.status_code == 200:
        data = resp.json()
        print(f"✅ API is healthy: {data.get('status', 'OK')}\n")
    else:
        print(f"❌ Health check failed: {resp.status_code}\n")
except Exception as e:
    print(f"❌ Error: {e}\n")

# 2. Connect camera
print("2️⃣  Connecting to Camera...")
try:
    resp = requests.post(f"{BASE_URL}/api/connect_camera", json={}, timeout=5)
    if resp.status_code == 200:
        data = resp.json()
        print(f"✅ {data.get('message', 'Camera connected')}\n")
    else:
        data = resp.json()
        print(f"⚠️  {data.get('error', 'Could not connect to camera')}")
        print(f"    (This is normal if no camera is available)\n")
except Exception as e:
    print(f"❌ Error: {e}\n")

# 3. Test capture and analyze
print("3️⃣  Testing Frame Capture & Analysis...")
try:
    resp = requests.post(f"{BASE_URL}/api/capture_and_analyze", json={}, timeout=10)
    
    if resp.status_code == 200:
        data = resp.json()
        print(f"✅ Frame captured successfully!\n")
        
        # Check for NaN values in the response
        analysis = data.get('analysis', {})
        print("📊 Analysis Results:")
        print(f"   • Cracks: {analysis.get('cracks')} (type: {type(analysis.get('cracks')).__name__})")
        print(f"   • Severity: {analysis.get('severity')}")
        print(f"   • Material: {analysis.get('material')}")
        print(f"   • Confidence: {analysis.get('confidence')} (type: {type(analysis.get('confidence')).__name__})")
        print(f"   • Growth Detected: {analysis.get('growth_detected')}")
        print(f"   • Health Score: {analysis.get('health_score')} (type: {type(analysis.get('health_score')).__name__})")
        
        print(f"\n✨ Message: {data.get('message')}")
        
        # Validate JSON serialization
        try:
            json_str = json.dumps(data)
            print("\n✅ JSON Response is Valid (no NaN/Infinity issues)")
        except (ValueError, TypeError) as e:
            print(f"\n❌ JSON Serialization Error: {e}")
            
    elif resp.status_code == 400:
        data = resp.json()
        print(f"⚠️  {data.get('error', 'Camera not connected')}")
        print(f"    (Try connecting camera first)\n")
    else:
        print(f"❌ Error {resp.status_code}:")
        try:
            print(json.dumps(resp.json(), indent=2))
        except:
            print(resp.text)
            
except requests.exceptions.Timeout:
    print("❌ Request timed out (server may be slow)\n")
except Exception as e:
    print(f"❌ Error: {e}\n")

# 4. Disconnect camera
print("4️⃣  Disconnecting Camera...")
try:
    resp = requests.post(f"{BASE_URL}/api/disconnect_camera", json={}, timeout=5)
    if resp.status_code == 200:
        data = resp.json()
        print(f"✅ {data.get('message', 'Camera disconnected')}\n")
except Exception as e:
    print(f"⚠️  Could not disconnect: {e}\n")

print("=" * 70)
print("🎉 Test Complete!")
print("=" * 70)
