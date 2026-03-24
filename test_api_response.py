#!/usr/bin/env python3
"""Test script to verify API is returning data to React frontend"""

import requests
import json
import base64
from PIL import Image
import io
import numpy as np

# Create a simple test image
test_image = Image.new('RGB', (225, 225), color='red')
img_buffer = io.BytesIO()
test_image.save(img_buffer, format='PNG')
img_buffer.seek(0)
img_base64 = base64.b64encode(img_buffer.getvalue()).decode('utf-8')

# Test the API
API_URL = 'http://localhost:5002'

print("=" * 60)
print("Testing API /api/analyze endpoint")
print("=" * 60)

try:
    response = requests.post(
        f'{API_URL}/api/analyze',
        json={
            'image': f'data:image/png;base64,{img_base64}',
            'px_to_cm_ratio': 0.1,
            'confidence_threshold': 0.3
        },
        timeout=30
    )
    
    print(f"\n✅ API Response Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"\n✅ Response JSON keys: {list(data.keys())}")
        
        if 'results' in data:
            print(f"\n✅ Results keys: {list(data['results'].keys())}")
        else:
            print("\n❌ ERROR: 'results' key missing from response")
        
        if 'output_images' in data:
            print(f"\n✅ Output images keys: {list(data['output_images'].keys())}")
            
            # Check if images are base64
            for key, value in data['output_images'].items():
                if value and isinstance(value, str):
                    if value.startswith('data:image'):
                        print(f"  ✅ {key}: Base64 image (length: {len(value)})")
                    else:
                        print(f"  ⚠️ {key}: Not a valid base64 image")
                else:
                    print(f"  ❌ {key}: Missing or invalid value")
        else:
            print("\n❌ ERROR: 'output_images' key missing from response")
        
        # Print sample of results structure
        if 'crack_detection' in data.get('results', {}):
            cd = data['results']['crack_detection']
            print(f"\n✅ Crack detection data: count={cd.get('count')}, details length={len(cd.get('details', []))}")
        
        if 'biological_growth' in data.get('results', {}):
            bg = data['results']['biological_growth']
            print(f"✅ Biological growth: growth_percentage={bg.get('growth_percentage')}%")
            
    else:
        print(f"\n❌ API Error: {response.status_code}")
        print(f"Response: {response.text}")
        
except Exception as e:
    print(f"\n❌ Error connecting to API: {e}")
    print("Make sure the API is running: python finalwebapp_api.py")

print("\n" + "=" * 60)
