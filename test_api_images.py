#!/usr/bin/env python3
"""
Quick test script to verify API is returning distinct processed images
"""
import requests
import base64
import json
from PIL import Image
import io
import sys

# Fix Unicode output for Windows
if sys.stdout.encoding != 'utf-8':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Create a simple test image
test_image = Image.new('RGB', (640, 640), color='blue')
test_image_bytes = io.BytesIO()
test_image.save(test_image_bytes, format='PNG')
test_image_base64 = base64.b64encode(test_image_bytes.getvalue()).decode('utf-8')
test_image_data_uri = f"data:image/png;base64,{test_image_base64}"

# Send to API
url = "http://localhost:5002/api/analyze"
payload = {
    "image": test_image_data_uri,
    "px_to_cm_ratio": 0.1,
    "confidence_threshold": 0.3
}

print("[*] Sending test image to API...")
response = requests.post(url, json=payload)

if response.status_code == 200:
    data = response.json()
    print("[OK] API responded with 200 OK")
    
    output_images = data.get('output_images', {})
    print(f"\n[INFO] Received {len(output_images)} processed images:")
    
    # Check if images are distinct
    image_hashes = {}
    for key, b64_data in output_images.items():
        if b64_data:
            # Take first 100 chars as hash
            hash_val = b64_data[:100]
            image_hashes[key] = hash_val
            print(f"\n  {key}: {b64_data[:80]}...")
    
    # Check uniqueness
    unique_hashes = len(set(image_hashes.values()))
    total_images = len(image_hashes)
    print(f"\n[STATS] Uniqueness Check:")
    print(f"  Total images: {total_images}")
    print(f"  Unique image hashes: {unique_hashes}")
    
    if unique_hashes == total_images:
        print("  [OK] All images are DISTINCT!")
    elif unique_hashes < total_images:
        print(f"  [WARNING] Only {unique_hashes}/{total_images} images are unique")
        print("  Some images may be duplicates")
    
    # Save sample images for manual inspection
    print("\n[*] Saving sample images to disk...")
    for key, b64_data in list(output_images.items())[:3]:
        if b64_data.startswith('data:image'):
            b64_data = b64_data.split(',')[1]
        
        try:
            img_data = base64.b64decode(b64_data)
            with open(f"sample_{key}.png", "wb") as f:
                f.write(img_data)
            print(f"  [OK] Saved: sample_{key}.png")
        except Exception as e:
            print(f"  [ERROR] Failed to save {key}: {e}")
    
else:
    print(f"[ERROR] API returned {response.status_code}: {response.text}")
