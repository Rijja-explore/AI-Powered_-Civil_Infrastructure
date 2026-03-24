#!/usr/bin/env python3
"""
Test script for InfraVision AI - Frame-wise Video Analysis
Verifies API endpoints and frame capture functionality
"""

import requests
import json
import base64
import cv2
from datetime import datetime

API_URL = "http://localhost:5002"

class VideoAnalysisTest:
    def __init__(self):
        self.results = []
        
    def log(self, message, status="INFO"):
        timestamp = datetime.now().strftime("%H:%M:%S")
        symbol = "✅" if status == "OK" else "❌" if status == "ERROR" else "⏳"
        print(f"{symbol} [{timestamp}] {message}")
        self.results.append({"time": timestamp, "message": message, "status": status})
    
    def test_health_check(self):
        """Test API is running"""
        try:
            response = requests.get(f"{API_URL}/api/health", timeout=5)
            if response.status_code == 200:
                self.log("✅ API Health Check PASSED", "OK")
                return True
            else:
                self.log(f"❌ API Health Check Failed: {response.status_code}", "ERROR")
                return False
        except Exception as e:
            self.log(f"❌ Cannot reach API: {str(e)}", "ERROR")
            return False
    
    def test_camera_connect(self):
        """Test camera connection"""
        try:
            response = requests.post(f"{API_URL}/api/connect_camera", json={}, timeout=5)
            data = response.json()
            if data.get("success"):
                self.log(f"✅ Camera Connected: {data.get('message')}", "OK")
                return True
            else:
                self.log(f"⏳ Camera Connection: {data.get('error')}", "ERROR")
                return False
        except Exception as e:
            self.log(f"❌ Camera Connection Failed: {str(e)}", "ERROR")
            return False
    
    def test_capture_and_analyze(self, num_frames=3):
        """Test frame capture and analysis"""
        self.log(f"Starting frame capture test ({num_frames} frames)...", "INFO")
        
        for i in range(num_frames):
            try:
                response = requests.post(
                    f"{API_URL}/api/capture_and_analyze",
                    json={},
                    timeout=10
                )
                
                if response.status_code == 200:
                    data = response.json()
                    
                    if data.get("success"):
                        analysis = data.get("analysis", {})
                        self.log(
                            f"Frame {i+1}: "
                            f"Cracks={analysis.get('cracks', '?')} | "
                            f"Health={analysis.get('health_score', '?')}% | "
                            f"Material={analysis.get('material', '?')}",
                            "OK"
                        )
                    else:
                        self.log(f"Frame {i+1}: {data.get('error')}", "ERROR")
                else:
                    self.log(f"Frame {i+1}: HTTP {response.status_code}", "ERROR")
            except Exception as e:
                self.log(f"Frame {i+1}: Exception - {str(e)}", "ERROR")
            
            if i < num_frames - 1:
                import time
                time.sleep(2)  # Wait 2 seconds between frames
        
        return True
    
    def test_camera_disconnect(self):
        """Test camera disconnection"""
        try:
            response = requests.post(f"{API_URL}/api/disconnect_camera", json={}, timeout=5)
            data = response.json()
            if data.get("success"):
                self.log(f"✅ Camera Disconnected", "OK")
                return True
            else:
                self.log(f"❌ Disconnect Failed: {data.get('error')}", "ERROR")
                return False
        except Exception as e:
            self.log(f"❌ Disconnect Error: {str(e)}", "ERROR")
            return False
    
    def run_all_tests(self):
        """Run all tests"""
        print("\n" + "="*60)
        print("  InfraVision AI - Frame-Wise Video Analysis Test")
        print("="*60 + "\n")
        
        # Test sequence
        self.log("Starting test suite...", "INFO")
        
        # 1. Health check
        if not self.test_health_check():
            self.log("Cannot continue without API", "ERROR")
            return False
        
        # 2. Connect camera
        if not self.test_camera_connect():
            self.log("Skipping frame capture (no camera)", "ERROR")
            self.print_summary()
            return False
        
        # 3. Capture frames
        self.test_capture_and_analyze(num_frames=3)
        
        # 4. Disconnect camera
        self.test_camera_disconnect()
        
        self.print_summary()
        return True
    
    def print_summary(self):
        """Print test summary"""
        print("\n" + "="*60)
        print("  TEST SUMMARY")
        print("="*60)
        
        passed = sum(1 for r in self.results if r["status"] == "OK")
        failed = sum(1 for r in self.results if r["status"] == "ERROR")
        
        print(f"\n✅ Passed: {passed}")
        print(f"❌ Failed: {failed}")
        print(f"Total: {len(self.results)}\n")
        
        if failed == 0:
            print("🎉 All tests passed! Frame-wise analysis ready to use.\n")
        else:
            print("⚠️  Some tests failed. Check errors above.\n")

if __name__ == "__main__":
    tester = VideoAnalysisTest()
    tester.run_all_tests()
