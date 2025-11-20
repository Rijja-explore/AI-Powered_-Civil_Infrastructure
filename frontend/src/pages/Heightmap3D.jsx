import React, { useState, Suspense } from "react";
import { Canvas, useLoader } from "@react-three/fiber";
import { OrbitControls, STLLoader } from "@react-three/drei";
import { Cube, Upload, RotateCw } from "lucide-react";
import "../styles/heightmap3d.css";

function Model({ url }) {
  const geometry = useLoader(STLLoader, url);
  return (
    <mesh geometry={geometry}>
      <meshPhongMaterial
        color="#4f46e5"
        wireframe={false}
        shininess={100}
      />
    </mesh>
  );
}

function LoadingSpinner() {
  return (
    <div style={{ display: "flex", alignItems: "center", justifyContent: "center", height: "100%", color: "#999" }}>
      <RotateCw size={32} style={{ animation: "spin 1s linear infinite" }} />
      <span style={{ marginLeft: "1rem" }}>Loading 3D Model...</span>
    </div>
  );
}

export default function Heightmap3D() {
  const [modelUrl, setModelUrl] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [fileName, setFileName] = useState(null);

  async function handleUpload(e) {
    const file = e.target.files[0];
    if (!file) return;

    setLoading(true);
    setError(null);
    setFileName(file.name);

    try {
      const formData = new FormData();
      formData.append("image", file);

      const res = await fetch("http://localhost:5002/api/generate-3d-heightmap", {
        method: "POST",
        body: formData,
      });

      if (!res.ok) {
        throw new Error(`Server error: ${res.status}`);
      }

      const blob = await res.blob();
      const url = URL.createObjectURL(blob);
      setModelUrl(url);
    } catch (err) {
      setError(`Failed to generate 3D model: ${err.message}`);
      console.error("Upload error:", err);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div style={{ padding: "2rem", minHeight: "100vh", background: "var(--bg-gradient)" }}>
      <div style={{ maxWidth: "1200px", margin: "0 auto" }}>
        {/* Header */}
        <div style={{ marginBottom: "2rem" }}>
          <h1 style={{ display: "flex", alignItems: "center", gap: "0.75rem", margin: 0, color: "var(--dark)", fontSize: "2rem", fontWeight: 700 }}>
            <Cube size={32} style={{ color: "#4f46e5" }} />
            3D Heightmap Generator
          </h1>
          <p style={{ margin: "0.5rem 0 0 0", color: "var(--secondary)", fontSize: "1rem" }}>
            Convert 2D structural images into interactive 3D heightmaps for advanced visualization
          </p>
        </div>

        {/* Upload Card */}
        <div className="card" style={{ marginBottom: "2rem" }}>
          <div className="card-header">
            <h2 style={{ margin: 0, display: "flex", alignItems: "center", gap: "0.6rem" }}>
              <Upload size={24} />
              Upload Structural Image
            </h2>
            <p style={{ margin: "0.25rem 0 0 0", color: "var(--secondary)", fontSize: "0.875rem" }}>
              Select a 2D image (JPG, PNG) to convert into a 3D heightmap STL file
            </p>
          </div>
          <div className="card-body">
            <div
              style={{
                display: "flex",
                flexDirection: "column",
                alignItems: "center",
                gap: "1.5rem",
                padding: "2rem",
                border: "2px dashed var(--glass-border)",
                borderRadius: "var(--border-radius)",
                backgroundColor: "rgba(79, 70, 229, 0.05)",
                cursor: "pointer",
                transition: "all 0.3s ease",
              }}
              onDragOver={(e) => {
                e.preventDefault();
                e.currentTarget.style.borderColor = "#4f46e5";
                e.currentTarget.style.backgroundColor = "rgba(79, 70, 229, 0.1)";
              }}
              onDragLeave={(e) => {
                e.currentTarget.style.borderColor = "var(--glass-border)";
                e.currentTarget.style.backgroundColor = "rgba(79, 70, 229, 0.05)";
              }}
              onDrop={(e) => {
                e.preventDefault();
                e.currentTarget.style.borderColor = "var(--glass-border)";
                e.currentTarget.style.backgroundColor = "rgba(79, 70, 229, 0.05)";
                if (e.dataTransfer.files.length > 0) {
                  const fileInput = document.querySelector('input[type="file"]');
                  fileInput.files = e.dataTransfer.files;
                  handleUpload({ target: { files: e.dataTransfer.files } });
                }
              }}
            >
              <Upload size={48} style={{ color: "#4f46e5", opacity: 0.7 }} />
              <div style={{ textAlign: "center" }}>
                <p style={{ margin: "0 0 0.5rem 0", fontWeight: 600, color: "var(--dark)" }}>
                  Drop your image here or click to browse
                </p>
                <p style={{ margin: 0, fontSize: "0.875rem", color: "var(--secondary)" }}>
                  Supported formats: JPG, PNG, GIF, BMP
                </p>
              </div>
              <input
                type="file"
                accept="image/*"
                onChange={handleUpload}
                style={{ display: "none" }}
                id="imageUpload"
              />
              <label
                htmlFor="imageUpload"
                style={{
                  padding: "0.75rem 1.5rem",
                  backgroundColor: "#4f46e5",
                  color: "white",
                  borderRadius: "var(--border-radius)",
                  cursor: "pointer",
                  fontWeight: 600,
                  transition: "background 0.3s ease",
                }}
                onMouseOver={(e) => (e.currentTarget.style.backgroundColor = "#3730a3")}
                onMouseOut={(e) => (e.currentTarget.style.backgroundColor = "#4f46e5")}
              >
                Choose File
              </label>
            </div>

            {/* File Name & Status */}
            {fileName && (
              <div style={{ marginTop: "1rem", padding: "1rem", backgroundColor: "rgba(79, 70, 229, 0.1)", borderRadius: "var(--border-radius)" }}>
                <p style={{ margin: 0, color: "var(--dark)", fontWeight: 600 }}>
                  📄 {fileName}
                </p>
              </div>
            )}

            {/* Loading State */}
            {loading && (
              <div style={{ marginTop: "1rem", padding: "1rem", textAlign: "center", color: "#666" }}>
                <RotateCw size={24} style={{ animation: "spin 1s linear infinite", marginBottom: "0.5rem" }} />
                <p style={{ margin: 0, fontWeight: 600 }}>Generating 3D heightmap... This may take a moment</p>
              </div>
            )}

            {/* Error State */}
            {error && (
              <div style={{ marginTop: "1rem", padding: "1rem", backgroundColor: "#fee2e2", border: "1px solid #fecaca", borderRadius: "var(--border-radius)", color: "#991b1b" }}>
                <p style={{ margin: 0, fontWeight: 600 }}>❌ {error}</p>
              </div>
            )}

            {/* Success State */}
            {modelUrl && !loading && (
              <div style={{ marginTop: "1rem", padding: "1rem", backgroundColor: "#dcfce7", border: "1px solid #bbf7d0", borderRadius: "var(--border-radius)", color: "#166534" }}>
                <p style={{ margin: 0, fontWeight: 600 }}>✅ 3D heightmap generated successfully! Scroll to explore.</p>
              </div>
            )}
          </div>
        </div>

        {/* 3D Viewer Card */}
        {modelUrl && (
          <div className="card">
            <div className="card-header">
              <h2 style={{ margin: 0, display: "flex", alignItems: "center", gap: "0.6rem" }}>
                <Cube size={24} />
                Interactive 3D Heightmap Viewer
              </h2>
              <p style={{ margin: "0.25rem 0 0 0", color: "var(--secondary)", fontSize: "0.875rem" }}>
                Use mouse to rotate, scroll to zoom, middle-click to pan
              </p>
            </div>
            <div className="card-body">
              <div style={{ height: "700px", borderRadius: "var(--border-radius)", overflow: "hidden", border: "1px solid var(--glass-border)" }}>
                <Canvas camera={{ position: [100, 100, 100], fov: 50 }}>
                  <ambientLight intensity={0.6} />
                  <directionalLight position={[10, 10, 10]} intensity={0.8} />
                  <pointLight position={[-10, -10, -10]} intensity={0.3} />
                  
                  <Suspense fallback={<LoadingSpinner />}>
                    <Model url={modelUrl} />
                  </Suspense>
                  
                  <OrbitControls
                    autoRotate={false}
                    autoRotateSpeed={4}
                    enableZoom={true}
                    enablePan={true}
                    enableRotate={true}
                  />
                </Canvas>
              </div>

              {/* Model Info */}
              <div style={{ marginTop: "1.5rem", padding: "1rem", backgroundColor: "var(--light)", borderRadius: "var(--border-radius)", display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(200px, 1fr))", gap: "1rem" }}>
                <div>
                  <p style={{ margin: 0, fontSize: "0.875rem", color: "var(--secondary)" }}>Resolution</p>
                  <p style={{ margin: "0.25rem 0 0 0", fontWeight: 600, color: "var(--dark)" }}>200 × 200 pixels</p>
                </div>
                <div>
                  <p style={{ margin: 0, fontSize: "0.875rem", color: "var(--secondary)" }}>Height Scale</p>
                  <p style={{ margin: "0.25rem 0 0 0", fontWeight: 600, color: "var(--dark)" }}>10.0 units</p>
                </div>
                <div>
                  <p style={{ margin: 0, fontSize: "0.875rem", color: "var(--secondary)" }}>Smoothing</p>
                  <p style={{ margin: "0.25rem 0 0 0", fontWeight: 600, color: "var(--dark)" }}>Gaussian (σ=1.0)</p>
                </div>
                <div>
                  <p style={{ margin: 0, fontSize: "0.875rem", color: "var(--secondary)" }}>Format</p>
                  <p style={{ margin: "0.25rem 0 0 0", fontWeight: 600, color: "var(--dark)" }}>STL (ASCII)</p>
                </div>
              </div>

              {/* Download Button */}
              <div style={{ marginTop: "1.5rem", display: "flex", gap: "1rem" }}>
                <button
                  onClick={() => {
                    const link = document.createElement("a");
                    link.href = modelUrl;
                    link.download = "heightmap.stl";
                    document.body.appendChild(link);
                    link.click();
                    document.body.removeChild(link);
                  }}
                  style={{
                    padding: "0.75rem 1.5rem",
                    backgroundColor: "#4f46e5",
                    color: "white",
                    border: "none",
                    borderRadius: "var(--border-radius)",
                    cursor: "pointer",
                    fontWeight: 600,
                    fontSize: "1rem",
                    transition: "background 0.3s ease",
                  }}
                  onMouseOver={(e) => (e.currentTarget.style.backgroundColor = "#3730a3")}
                  onMouseOut={(e) => (e.currentTarget.style.backgroundColor = "#4f46e5")}
                >
                  📥 Download STL File
                </button>
                <button
                  onClick={() => {
                    setModelUrl(null);
                    setFileName(null);
                  }}
                  style={{
                    padding: "0.75rem 1.5rem",
                    backgroundColor: "#e5e7eb",
                    color: "var(--dark)",
                    border: "none",
                    borderRadius: "var(--border-radius)",
                    cursor: "pointer",
                    fontWeight: 600,
                    fontSize: "1rem",
                    transition: "background 0.3s ease",
                  }}
                  onMouseOver={(e) => (e.currentTarget.style.backgroundColor = "#d1d5db")}
                  onMouseOut={(e) => (e.currentTarget.style.backgroundColor = "#e5e7eb")}
                >
                  🔄 Generate New
                </button>
              </div>
            </div>
          </div>
        )}

        {/* Features Section */}
        <div style={{ marginTop: "3rem", padding: "2rem", backgroundColor: "var(--light)", borderRadius: "var(--border-radius)", border: "1px solid var(--glass-border)" }}>
          <h3 style={{ margin: "0 0 1rem 0", color: "var(--dark)", fontSize: "1.25rem", fontWeight: 600 }}>
            ✨ Features
          </h3>
          <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(250px, 1fr))", gap: "1.5rem" }}>
            <div>
              <p style={{ margin: 0, fontWeight: 600, color: "var(--dark)", display: "flex", alignItems: "center", gap: "0.5rem" }}>
                🎨 Automatic Conversion
              </p>
              <p style={{ margin: "0.5rem 0 0 0", fontSize: "0.875rem", color: "var(--secondary)" }}>
                Converts 2D structural images to 3D heightmaps automatically using brightness values
              </p>
            </div>
            <div>
              <p style={{ margin: 0, fontWeight: 600, color: "var(--dark)", display: "flex", alignItems: "center", gap: "0.5rem" }}>
                🔍 Interactive Viewer
              </p>
              <p style={{ margin: "0.5rem 0 0 0", fontSize: "0.875rem", color: "var(--secondary)" }}>
                Rotate, zoom, and pan to explore 3D structure from all angles in real-time
              </p>
            </div>
            <div>
              <p style={{ margin: 0, fontWeight: 600, color: "var(--dark)", display: "flex", alignItems: "center", gap: "0.5rem" }}>
                💾 STL Export
              </p>
              <p style={{ margin: "0.5rem 0 0 0", fontSize: "0.875rem", color: "var(--secondary)" }}>
                Download STL files for 3D printing, CAD analysis, or further processing
              </p>
            </div>
            <div>
              <p style={{ margin: 0, fontWeight: 600, color: "var(--dark)", display: "flex", alignItems: "center", gap: "0.5rem" }}>
                ⚙️ Advanced Processing
              </p>
              <p style={{ margin: "0.5rem 0 0 0", fontSize: "0.875rem", color: "var(--secondary)" }}>
                Gaussian smoothing, automatic scaling, and intelligent mesh generation
              </p>
            </div>
            <div>
              <p style={{ margin: 0, fontWeight: 600, color: "var(--dark)", display: "flex", alignItems: "center", gap: "0.5rem" }}>
                🏗️ Infrastructure Ready
              </p>
              <p style={{ margin: "0.5rem 0 0 0", fontSize: "0.875rem", color: "var(--secondary)" }}>
                Perfect for structural health monitoring and damage visualization
              </p>
            </div>
            <div>
              <p style={{ margin: 0, fontWeight: 600, color: "var(--dark)", display: "flex", alignItems: "center", gap: "0.5rem" }}>
                🚀 Real-time Processing
              </p>
              <p style={{ margin: "0.5rem 0 0 0", fontSize: "0.875rem", color: "var(--secondary)" }}>
                Fast conversion with instant 3D preview and visualization
              </p>
            </div>
          </div>
        </div>
      </div>

      <style>{`
        @keyframes spin {
          from { transform: rotate(0deg); }
          to { transform: rotate(360deg); }
        }
      `}</style>
    </div>
  );
}
