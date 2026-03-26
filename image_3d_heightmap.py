"""
FINAL PIPELINE: 2D image → processed overlay → 3D colored GLB heightmap

What it does:
    1) Load a normal 2D image
    2) Create:
        - heatmap from grayscale
        - Canny edge map
        - overlay = original + heatmap + edges
    3) Use grayscale as heightmap → build 3D mesh
    4) Use overlay image as vertex colors
    5) Export .glb you can view & rotate (e.g. Blender, Three.js, React Three Fiber)
"""

import numpy as np
from PIL import Image
import cv2
from scipy.ndimage import gaussian_filter
import trimesh
import os


# ==============================================================
# FUNCTION 1: CREATE HEATMAP + CANNY + ORIGINAL OVERLAY
# ==============================================================

def make_processed_image(input_path, resize_to=(300, 300)):
    """
    Process input image to create a colored texture map with Canny edges overlaid on heatmap.
    
    Creates striking visualization by:
    1. Generating colorful JET heatmap as background (blue→green→yellow→red)
    2. Detecting Canny edges (sharp boundaries)
    3. Overlaying edges as dark/magenta lines ON TOP of heatmap
    
    This creates the effect seen in thermal/satellite imagery where structure
    boundaries are clearly visible over the colored temperature/elevation map.
    
    Args:
        input_path: Path to input image
        resize_to: Tuple (width, height) for resizing
    
    Returns:
        combined: RGB image with heatmap + Canny edges overlay (final texture for 3D)
        gray: Grayscale version for heightmap Z-coordinate generation
    """
    try:
        # --- Load and resize image ---
        print(f"[3D] Loading image from: {input_path}")
        img = Image.open(input_path).convert("RGB")
        print(f"[3D] Original size: {img.size}")
        
        img = img.resize(resize_to, Image.LANCZOS)
        print(f"[3D] Resized to: {img.size}")
        img_np = np.array(img, dtype=np.uint8)    # (H, W, 3), uint8
        print(f"[3D] Image array shape: {img_np.shape}")

        # --- Convert to grayscale (used for both heatmap and heightmap) ---
        gray = cv2.cvtColor(img_np, cv2.COLOR_RGB2GRAY)  # (H, W), uint8
        print(f"[3D] Grayscale shape: {gray.shape}")

        # --- Create colorful JET heatmap background ---
        heatmap_bgr = cv2.applyColorMap(gray, cv2.COLORMAP_JET)   # BGR format from intensity
        heatmap_rgb = cv2.cvtColor(heatmap_bgr, cv2.COLOR_BGR2RGB)  # Convert to RGB
        print(f"[3D] Heatmap created, shape: {heatmap_rgb.shape}")

        # --- Detect Canny edges (sharp, high-contrast boundaries) ---
        edges_binary = cv2.Canny(gray, 80, 160)   # (H, W), binary: 255 where edge, 0 elsewhere
        print(f"[3D] Canny edges detected")

        # --- Create edge overlay with magenta/purple tone for striking contrast ---
        # Start with the heatmap as base
        combined = heatmap_rgb.astype(np.float32)
        
        # Where edges exist, overlay with dark magenta/purple
        # This creates the striking effect of dark lines over colored background
        edge_mask = edges_binary / 255.0  # Convert to 0-1 range
        edge_mask = edge_mask[:, :, np.newaxis]  # Add channel dimension (H, W, 1)
        
        # Define edge color: dark purple/magenta for maximum contrast
        edge_color = np.array([80, 0, 150], dtype=np.float32)  # Dark purple: R=80, G=0, B=150
        
        # Blend: where edge_mask=1, use edge_color; where edge_mask=0, use heatmap
        combined = combined * (1 - edge_mask) + edge_color * edge_mask
        
        # Clamp and convert back to uint8
        combined = np.clip(combined, 0, 255).astype(np.uint8)
        print(f"[3D] Combined image created, shape: {combined.shape}")

        return combined, gray
    
    except Exception as e:
        print(f"[3D ERROR] Failed to process image: {e}")
        import traceback
        traceback.print_exc()
        raise


# ==============================================================
# FUNCTION 2: CONVERT TO 3D HEIGHTMAP + ADD TEXTURE COLORS
# ==============================================================

def make_3d_glb(
    gray_img,
    color_img,
    output_path="output.glb",
    height_scale=12.0,
    smooth_sigma=1.2,
    flip_y=True
):
    """
    Converts grayscale heightmap → 3D mesh (GLB) with vertex colors from color_img.

    Args:
        gray_img    : (H, W) uint8 or float, used as height
        color_img   : (H, W, 3) uint8, used as vertex colors
        output_path : path to .glb file to save
        height_scale: how tall the displacement will be
        smooth_sigma: Gaussian blur strength (0 = no smoothing)
        flip_y      : flip Y axis so mesh appears upright in many viewers
    """
    try:
        print(f"[3D] Starting 3D GLB creation...")
        
        # Ensure numpy arrays
        gray = np.array(gray_img).astype(float)
        color = np.array(color_img).astype(np.uint8)
        
        print(f"[3D] Gray array shape: {gray.shape}, dtype: {gray.dtype}")
        print(f"[3D] Color array shape: {color.shape}, dtype: {color.dtype}")

        h, w = gray.shape
        assert color.shape[0] == h and color.shape[1] == w, \
            f"gray_img and color_img must have same height/width. Got gray: {gray.shape}, color: {color.shape}"

        # --- Smooth height to reduce noise ---
        if smooth_sigma > 0:
            print(f"[3D] Applying Gaussian smoothing (σ={smooth_sigma})...")
            gray = gaussian_filter(gray, sigma=smooth_sigma)
            print(f"[3D] Smoothing complete")

        # --- Normalize height 0..1 ---
        arr_min, arr_max = gray.min(), gray.max()
        print(f"[3D] Height range: [{arr_min:.2f}, {arr_max:.2f}]")
        norm = (gray - arr_min) / (arr_max - arr_min + 1e-9)
        height = norm * height_scale
        print(f"[3D] Normalized height range: [{height.min():.2f}, {height.max():.2f}]")

        # --- Create vertices (grid) ---
        print(f"[3D] Creating vertex grid ({h}x{w})...")
        verts = np.zeros((h * w, 3), dtype=float)
        for y in range(h):
            for x in range(w):
                z = float(height[y, x])
                idx = y * w + x
                if flip_y:
                    verts[idx] = [x, (h - 1 - y), z]
                else:
                    verts[idx] = [x, y, z]
        print(f"[3D] Vertices created: {verts.shape}")

        # --- Create faces (two triangles per pixel-square) ---
        print(f"[3D] Creating face indices...")
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
        faces = np.array(faces, dtype=np.int64)
        print(f"[3D] Faces created: {faces.shape}")

        # --- Flatten color image into vertex colors (RGBA) ---
        print(f"[3D] Creating vertex colors...")
        color_flat = color.reshape(-1, 3)                 # (N, 3)
        alpha = np.full((color_flat.shape[0], 1), 255,
                        dtype=np.uint8)                   # (N, 1)
        colors = np.hstack([color_flat, alpha])           # (N, 4)
        print(f"[3D] Vertex colors created: {colors.shape}")

        # --- Build mesh & export GLB ---
        print(f"[3D] Building trimesh object...")
        mesh = trimesh.Trimesh(
            vertices=verts,
            faces=faces,
            vertex_colors=colors,
            process=False
        )
        print(f"[3D] Mesh created: {mesh}")

        print(f"[3D] Exporting to GLB format: {output_path}")
        mesh.export(output_path)
        print(f"[INFO] Saved 3D GLB model to: {os.path.abspath(output_path)}")
    
    except Exception as e:
        print(f"[3D ERROR] Failed to create 3D GLB: {e}")
        import traceback
        traceback.print_exc()
        raise


# ==============================================================
# WRAPPER FUNCTIONS FOR API INTEGRATION
# ==============================================================

def generate_3d_glb_from_image(
    input_image_path,
    output_glb_path,
    resize_to=(300, 300),
    height_scale=12.0,
    smooth_sigma=1.2
):
    """
    High-level function to generate 3D GLB from image file.
    
    Args:
        input_image_path: Path to input image
        output_glb_path: Path for output GLB file
        resize_to: Resolution tuple (width, height)
        height_scale: Height multiplier
        smooth_sigma: Gaussian smoothing strength
    
    Returns:
        output_glb_path: Path to generated file
    """
    try:
        print(f"[3D] Starting 3D GLB generation from image")
        print(f"[3D] Input: {input_image_path}")
        print(f"[3D] Output: {output_glb_path}")
        
        # Process image (creates overlay + grayscale)
        print(f"[3D] Step 1: Processing image...")
        combined, gray = make_processed_image(
            input_image_path,
            resize_to=resize_to
        )
        print(f"[3D] Step 1 complete: combined shape={combined.shape}, gray shape={gray.shape}")
        
        # Generate 3D model with vertex colors
        print(f"[3D] Step 2: Generating 3D model...")
        make_3d_glb(
            gray,
            combined,
            output_path=output_glb_path,
            height_scale=height_scale,
            smooth_sigma=smooth_sigma,
            flip_y=True
        )
        print(f"[3D] Step 2 complete: GLB exported")
        
        return output_glb_path
    
    except Exception as e:
        print(f"[3D ERROR] Failed to generate 3D GLB from image: {e}")
        import traceback
        traceback.print_exc()
        raise


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
        color_array: 3D numpy array for colors (H x W x 3)
        output_glb_path: Path for output GLB
        height_scale: Height scale factor
        smooth_sigma: Smoothing parameter
    
    Returns:
        output_glb_path: Path to generated file
    """
    # Ensure proper data types
    height_array = np.array(height_array).astype(float)
    color_array = np.array(color_array).astype(np.uint8)
    
    make_3d_glb(
        height_array,
        color_array,
        output_path=output_glb_path,
        height_scale=height_scale,
        smooth_sigma=smooth_sigma,
        flip_y=True
    )
    
    return output_glb_path


# ==============================================================
# EXAMPLE USAGE
# ==============================================================

if __name__ == "__main__":
    # Example: Process crack image and generate 3D model
    input_image = "crack_sample.jpg"  # Replace with your image path
    out_glb = "crack_3d_model.glb"
    out_overlay = "processed_overlay.png"
    
    # Check if input exists
    if not os.path.exists(input_image):
        print(f"[ERROR] Input image not found: {input_image}")
        print("[INFO] Please place an image file and update the path")
        exit(1)
    
    print(f"[INFO] Processing image: {input_image}")
    
    # Step 1: Create processed overlay + grayscale heightmap
    processed_img, gray = make_processed_image(input_image, resize_to=(300, 300))
    
    # Save processed overlay for inspection
    Image.fromarray(processed_img).save(out_overlay)
    print(f"[INFO] Saved processed overlay to: {os.path.abspath(out_overlay)}")
    
    # Step 2: Generate 3D GLB model
    make_3d_glb(
        gray, 
        processed_img, 
        output_path=out_glb,
        height_scale=15.0,  # Adjust for more/less height variation
        smooth_sigma=1.0    # Adjust for more/less smoothing
    )
    
    print(f"[SUCCESS] 3D pipeline complete!")
    print(f"[INFO] Generated files:")
    print(f"  - 3D Model: {os.path.abspath(out_glb)}")
    print(f"  - Overlay: {os.path.abspath(out_overlay)}")
    print(f"[INFO] You can now:")
    print(f"  - Open {out_glb} in Blender, 3D Viewer, or Three.js")
    print(f"  - Use in React Three Fiber with: useLoader(GLTFLoader, '{out_glb}')")