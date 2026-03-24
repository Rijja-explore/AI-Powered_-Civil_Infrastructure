#!/usr/bin/env python3
"""Test the /api/analyze_video endpoint"""
import requests
import cv2
import numpy as np
import os
import tempfile

BASE_URL = "http://localhost:5002"

print("=" * 70)
print("🧪 Testing /api/analyze_video Endpoint")
print("=" * 70)

# Create a small test video (2 seconds, 24 fps = 48 frames)
print("\n1️⃣  Creating Test Video File...")
try:
    # Create temp video
    temp_dir = tempfile.gettempdir()
    test_video_path = os.path.join(temp_dir, "test_video.mp4")
    
    # Create video with OpenCV
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(test_video_path, fourcc, 24.0, (640, 480))
    
    # Generate 48 frames (2 seconds at 24fps)
    for i in range(48):
        # Create a frame with some content
        frame = np.ones((480, 640, 3), dtype=np.uint8) * (100 + i)
        # Add some noise to simulate cracks
        for _ in range(5):
            pt1 = (np.random.randint(0, 640), np.random.randint(0, 480))
            pt2 = (np.random.randint(0, 640), np.random.randint(0, 480))
            cv2.line(frame, pt1, pt2, (50, 50, 50), 2)
        out.write(frame)
    
    out.release()
    print(f"✅ Test video created: {test_video_path}")
    print(f"   Size: {os.path.getsize(test_video_path) / 1024:.1f} KB\n")
except Exception as e:
    print(f"❌ Failed to create test video: {e}\n")
    exit(1)

# Test the endpoint
print("2️⃣  Uploading and Analyzing Video...")
try:
    with open(test_video_path, 'rb') as f:
        files = {'video': f}
        data = {
            'analysis_type': 'comprehensive',
            'px_to_cm_ratio': '0.1',
            'confidence_threshold': '0.3'
        }
        
        response = requests.post(
            f"{BASE_URL}/api/analyze_video",
            files=files,
            data=data,
            timeout=60
        )
    
    print(f"✅ Response Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"\n📊 Analysis Results:")
        print(f"   • Total Frames: {data.get('total_frames', 'N/A')}")
        print(f"   • Frames Processed: {data.get('frames_processed', 'N/A')}")
        print(f"   • FPS: {data.get('fps', 'N/A')}")
        print(f"   • Duration: {data.get('analysis_duration', 'N/A')} seconds")
        
        # Check frame results
        frame_results = data.get('frame_results', {})
        print(f"\n🎬 Frame Results:")
        print(f"   • Type: {type(frame_results).__name__}")
        print(f"   • Count: {len(frame_results)}")
        
        if isinstance(frame_results, dict):
            # Show first frame
            if frame_results:
                first_key = list(frame_results.keys())[0]
                first_frame = frame_results[first_key]
                print(f"\n   First Frame (Key: {first_key}):")
                print(f"     - Cracks: {first_frame.get('crack_detection', {}).get('count', 'N/A')}")
                print(f"     - Material: {first_frame.get('material_analysis', {}).get('predicted_material', 'N/A')}")
                print(f"     - Growth %: {first_frame.get('biological_growth', {}).get('growth_percentage', 'N/A')}")
        
        # Check summary
        summary = data.get('comprehensive_summary', {})
        print(f"\n📈 Comprehensive Summary:")
        print(f"   • Total Cracks: {summary.get('total_cracks_detected', 'N/A')}")
        print(f"   • Avg Health: {summary.get('average_structural_health', 'N/A')}")
        print(f"   • Risk Level: {summary.get('risk_level', 'N/A')}")
        
        print(f"\n✅ Video Analysis Successful!\n")
    else:
        error_data = response.json() if response.headers.get('content-type') == 'application/json' else {'error': response.text}
        print(f"❌ Error {response.status_code}:")
        print(f"   {error_data.get('error', error_data)}\n")
        
except requests.exceptions.Timeout:
    print(f"❌ Request timed out after 60 seconds\n")
except Exception as e:
    print(f"❌ Error: {e}\n")

# Cleanup
print("3️⃣  Cleanup...")
try:
    os.remove(test_video_path)
    print(f"✅ Test video deleted\n")
except:
    pass

print("=" * 70)
print("✨ Test Complete!")
print("=" * 70)
