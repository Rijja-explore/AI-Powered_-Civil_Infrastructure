# --------------------------------------------------------------
# HEIGHTMAP + TEXTURE 3D MODEL GENERATOR (GLB FORMAT)
# Generates textured 3D GLB models from 2D images
# Requires: pip install pillow numpy trimesh scipy opencv-python matplotlib
# --------------------------------------------------------------

import numpy as np
from PIL import Image
import cv2
from scipy.ndimage import gaussian_filter
import trimesh
from trimesh.exchange import gltf
import os
import tempfile


def make_processed_image(input_path, resize_to=(300, 300)):
    """
    Process input image to create a colored texture map.
    
    Args:
        input_path: Path to input image
        resize_to: Tuple (width, height) for resizing
    
    Returns:
        combined: RGB image with heatmap + edges
        gray: Grayscale version for heightmap
    """
    img = Image.open(input_path).convert("RGB")
    img = img.resize(resize_to, Image.LANCZOS)
    img_np = np.array(img)

    # Convert to grayscale for heightmap
    gray = cv2.cvtColor(img_np, cv2.COLOR_RGB2GRAY)

    # Apply jet colormap for heatmap visualization
    heatmap = cv2.applyColorMap(gray, cv2.COLORMAP_JET)
    heatmap = cv2.cvtColor(heatmap, cv2.COLOR_BGR2RGB)

    # Extract edges for detail
    edges = cv2.Canny(gray, 80, 160)
    edges_rgb = np.zeros_like(img_np)
    edges_rgb[..., 0] = edges  # Red channel for edges

    # Combine heatmap and edges for rich texture
    combined = (
        (0.5 * heatmap.astype(float)) +
        (1 * edges_rgb.astype(float))
    )

    combined = np.clip(combined, 0, 255).astype(np.uint8)

    return combined, gray


def make_3d_glb(
    gray_img,
    color_img,
    output_path="output.glb",
    height_scale=12.0,
    smooth_sigma=1.2,
    flip_y=True
):
    """
    Convert grayscale heightmap to 3D GLB model with texture.
    
    Args:
        gray_img: Grayscale image for height values
        color_img: RGB image for texture/color
        output_path: Path to save GLB file
        height_scale: Scale factor for height
        smooth_sigma: Gaussian smoothing sigma
        flip_y: Whether to flip Y axis
    
    Returns:
        output_path: Path to generated GLB file
    """
    # Apply smoothing to create smooth surface
    if smooth_sigma > 0:
        gray_img = gaussian_filter(gray_img, sigma=smooth_sigma)

    # Normalize grayscale to 0-1 range
    arr_min, arr_max = gray_img.min(), gray_img.max()
    norm = (gray_img - arr_min) / (arr_max - arr_min + 1e-9)
    height = norm * height_scale
    h, w = height.shape

    # Create vertex positions
    verts = np.zeros((h * w, 3), dtype=np.float32)
    for y in range(h):
        for x in range(w):
            z = float(height[y, x])
            if flip_y:
                verts[y * w + x] = [x, (h - 1 - y), z]
            else:
                verts[y * w + x] = [x, y, z]

    # Create triangle faces
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
    faces = np.array(faces, dtype=np.uint32)

    # Prepare vertex colors from color image
    color_img_resized = color_img.reshape(-1, 3)
    
    # Add alpha channel (full opacity)
    colors = np.hstack([
        color_img_resized.astype(np.uint8),
        np.full((color_img_resized.shape[0], 1), 255, dtype=np.uint8)
    ])

    # Create mesh
    mesh = trimesh.Trimesh(
        vertices=verts,
        faces=faces,
        vertex_colors=colors,
        process=False
    )

    # Compute vertex normals for better lighting
    mesh.vertex_normals  # Trigger computation
    
    # Export as GLB (binary GLTF format)
    mesh.export(output_path, file_type='glb')
    
    return output_path


def generate_3d_glb_from_image(
    input_image_path,
    output_glb_path,
    resize_to=(300, 300),
    height_scale=12.0,
    smooth_sigma=1.2
):
    """
    High-level function to generate 3D GLB from image.
    
    Args:
        input_image_path: Path to input image
        output_glb_path: Path for output GLB file
        resize_to: Size for resizing
        height_scale: Height scale factor
        smooth_sigma: Smoothing parameter
    
    Returns:
        output_glb_path: Path to generated file
    """
    # Process image
    combined, gray = make_processed_image(input_image_path, resize_to=resize_to)
    
    # Generate 3D model
    result = make_3d_glb(
        gray,
        combined,
        output_path=output_glb_path,
        height_scale=height_scale,
        smooth_sigma=smooth_sigma,
        flip_y=True
    )
    
    return result


# Alternative: Generate from existing arrays
def generate_3d_glb_from_arrays(
    height_array,
    color_array,
    output_glb_path,
    height_scale=12.0,
    smooth_sigma=1.2
):
    """
    Generate 3D GLB directly from numpy arrays.
    
    Args:
        height_array: 2D numpy array for heights
        color_array: 3D numpy array for colors (H x W x 3 or H x W x 4)
        output_glb_path: Path for output GLB
        height_scale: Height scale factor
        smooth_sigma: Smoothing parameter
    
    Returns:
        output_glb_path: Path to generated file
    """
    # Ensure proper data types
    height_array = height_array.astype(np.float32)
    color_array = color_array.astype(np.uint8)
    
    return make_3d_glb(
        height_array,
        color_array,
        output_path=output_glb_path,
        height_scale=height_scale,
        smooth_sigma=smooth_sigma,
        flip_y=True
    )
