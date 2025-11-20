# image_to_heightmap.py
# 2D Image to 3D Heightmap STL Generator
# Requirements: pip install pillow numpy trimesh scipy

import numpy as np
from PIL import Image
import trimesh
from scipy.ndimage import gaussian_filter

def image_to_stl(input_image_path, output_stl_path,
                 resize_to=(200, 200),
                 height_scale=10.0,
                 smooth_sigma=1.0,
                 flip_y=True):
    """
    Convert a 2D image to a 3D STL heightmap.
    
    Args:
        input_image_path: Path to input image
        output_stl_path: Path to save output STL file
        resize_to: Tuple (width, height) for resizing
        height_scale: Scale factor for height values
        smooth_sigma: Gaussian smoothing parameter (0 = no smoothing)
        flip_y: Whether to flip Y axis
    
    Returns:
        Path to saved STL file
    """
    
    # Load image and convert to grayscale
    img = Image.open(input_image_path).convert("L")
    img = img.resize(resize_to, Image.LANCZOS)
    arr = np.array(img).astype(float)

    # Optionally smooth to remove noise
    if smooth_sigma > 0:
        arr = gaussian_filter(arr, sigma=smooth_sigma)

    # Normalize to 0..1
    arr_min, arr_max = arr.min(), arr.max()
    if arr_max - arr_min < 1e-8:
        norm = np.zeros_like(arr)
    else:
        norm = (arr - arr_min) / (arr_max - arr_min)

    # Create height values
    height = norm * height_scale

    h, w = height.shape

    # Build vertices (grid)
    verts = np.zeros((h * w, 3), dtype=float)
    for y in range(h):
        for x in range(w):
            z = float(height[y, x])
            if flip_y:
                verts[y * w + x] = [x, (h - 1 - y), z]
            else:
                verts[y * w + x] = [x, y, z]

    # Build faces (triangles)
    faces = []
    for y in range(h - 1):
        for x in range(w - 1):
            i = y * w + x
            a = i
            b = i + 1
            c = i + w
            d = i + w + 1
            faces.append([a, b, c])
            faces.append([b, d, c])
    faces = np.array(faces)

    # Create and export mesh
    mesh = trimesh.Trimesh(vertices=verts, faces=faces, process=True)
    mesh.export(output_stl_path)

    return output_stl_path
