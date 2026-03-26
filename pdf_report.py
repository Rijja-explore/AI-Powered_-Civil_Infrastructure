"""
PDF Report Generation Module
Generates PDF reports from analysis results
"""

import io
import tempfile
import os
from datetime import datetime
from PIL import Image
import numpy as np

try:
    from reportlab.lib.pagesizes import letter, A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image as RLImage, PageBreak, Table, TableStyle
    from reportlab.lib import colors
    REPORTLAB_AVAILABLE = True
except ImportError:
    print("⚠️ reportlab not available. PDF reports will use fallback mode.")
    REPORTLAB_AVAILABLE = False


def save_image_to_temp(image_np, format='PNG'):
    """
    Save a numpy image to a temporary file.
    
    Args:
        image_np: numpy array image
        format: image format (PNG, JPEG, etc.)
    
    Returns:
        Path to temporary image file
    """
    try:
        if image_np is None:
            return None
        
        # Convert numpy array to PIL Image
        if len(image_np.shape) == 2:
            # Grayscale
            pil_image = Image.fromarray(image_np)
        else:
            # Color image - handle BGR to RGB conversion if needed
            pil_image = Image.fromarray(image_np)
        
        # Save to temporary file
        temp_file = tempfile.NamedTemporaryFile(suffix=f'.{format.lower()}', delete=False)
        pil_image.save(temp_file.name, format=format)
        
        return temp_file.name
    except Exception as e:
        print(f"Error saving image to temp file: {e}")
        return None


def generate_pdf_report(
    analysis_results,
    crack_image=None,
    growth_image=None,
    depth_image=None,
    edge_image=None,
    segmentation_image=None,
    output_path=None
):
    """
    Generate a comprehensive PDF report from analysis results.
    
    Args:
        analysis_results: Dictionary containing analysis data
        crack_image: Optional crack detection visualization
        growth_image: Optional biological growth detection visualization
        depth_image: Optional depth estimation visualization
        edge_image: Optional edge detection visualization
        segmentation_image: Optional segmentation visualization
        output_path: Path to save PDF (if None, returns BytesIO buffer)
    
    Returns:
        BytesIO buffer or file path depending on output_path
    """
    try:
        print("[PDF] Generating PDF report...")
        
        # If reportlab is not available, return a simple buffer
        if not REPORTLAB_AVAILABLE:
            print("[PDF] reportlab not available - using fallback mode (empty PDF)")
            buffer = io.BytesIO()
            buffer.write(b'%PDF-1.4\n')
            buffer.write(b'Fallback PDF - Full reportlab module required for complete report\n')
            buffer.seek(0)
            return buffer
        
        # Create PDF document
        buffer = io.BytesIO() if output_path is None else None
        pdf_path = output_path or buffer
        
        doc = SimpleDocTemplate(
            pdf_path,
            pagesize=letter,
            rightMargin=0.75*inch,
            leftMargin=0.75*inch,
            topMargin=0.75*inch,
            bottomMargin=0.75*inch
        )
        
        # Container for PDF elements
        elements = []
        
        # Define styles
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1f2937'),
            spaceAfter=30,
            alignment=1  # Center alignment
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=14,
            textColor=colors.HexColor('#374151'),
            spaceAfter=12,
            spaceBefore=12
        )
        
        # Add title
        elements.append(Paragraph("Infrastructure Health Analysis Report", title_style))
        elements.append(Spacer(1, 0.2*inch))
        
        # Add timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        elements.append(Paragraph(f"<i>Generated: {timestamp}</i>", styles['Normal']))
        elements.append(Spacer(1, 0.3*inch))
        
        # Add analysis summary
        elements.append(Paragraph("Analysis Summary", heading_style))
        
        if analysis_results:
            # Create summary table
            summary_data = [['Metric', 'Value']]
            
            if 'crack_details' in analysis_results:
                crack_count = len(analysis_results.get('crack_details', []))
                summary_data.append(['Cracks Detected', str(crack_count)])
            
            if 'growth_analysis' in analysis_results:
                growth = analysis_results['growth_analysis']
                summary_data.append(['Biological Growth', f"{growth.get('growth_percentage', 0):.1f}%"])
            
            if 'material_analysis' in analysis_results:
                material = analysis_results['material_analysis']
                summary_data.append(['Primary Material', material.get('predicted_material', 'Unknown')])
                summary_data.append(['Material Confidence', f"{material.get('confidence', 0)*100:.1f}%"])
            
            if summary_data and len(summary_data) > 1:
                table = Table(summary_data, colWidths=[3*inch, 2*inch])
                table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#e5e7eb')),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 11),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black)
                ]))
                elements.append(table)
                elements.append(Spacer(1, 0.3*inch))
        
        # Add images if available
        image_added = False
        
        if crack_image is not None:
            elements.append(Paragraph("Crack Detection", heading_style))
            temp_path = save_image_to_temp(crack_image) if isinstance(crack_image, np.ndarray) else crack_image
            if temp_path and os.path.exists(temp_path):
                img = RLImage(temp_path, width=5*inch, height=4*inch)
                elements.append(img)
                elements.append(Spacer(1, 0.2*inch))
                image_added = True
        
        if growth_image is not None:
            elements.append(Paragraph("Biological Growth Detection", heading_style))
            temp_path = save_image_to_temp(growth_image) if isinstance(growth_image, np.ndarray) else growth_image
            if temp_path and os.path.exists(temp_path):
                img = RLImage(temp_path, width=5*inch, height=4*inch)
                elements.append(img)
                elements.append(Spacer(1, 0.2*inch))
                image_added = True
        
        if depth_image is not None:
            elements.append(Paragraph("Depth Analysis", heading_style))
            temp_path = save_image_to_temp(depth_image) if isinstance(depth_image, np.ndarray) else depth_image
            if temp_path and os.path.exists(temp_path):
                img = RLImage(temp_path, width=5*inch, height=4*inch)
                elements.append(img)
                elements.append(Spacer(1, 0.2*inch))
                image_added = True
        
        if edge_image is not None:
            elements.append(Paragraph("Edge Detection", heading_style))
            temp_path = save_image_to_temp(edge_image) if isinstance(edge_image, np.ndarray) else edge_image
            if temp_path and os.path.exists(temp_path):
                img = RLImage(temp_path, width=5*inch, height=4*inch)
                elements.append(img)
                elements.append(Spacer(1, 0.2*inch))
                image_added = True
        
        if segmentation_image is not None:
            elements.append(Paragraph("AI Segmentation", heading_style))
            temp_path = save_image_to_temp(segmentation_image) if isinstance(segmentation_image, np.ndarray) else segmentation_image
            if temp_path and os.path.exists(temp_path):
                img = RLImage(temp_path, width=5*inch, height=4*inch)
                elements.append(img)
                elements.append(Spacer(1, 0.2*inch))
                image_added = True
        
        # Add footer
        elements.append(Spacer(1, 0.5*inch))
        elements.append(Paragraph(
            "<i>This is an automated infrastructure health analysis report generated by InfraVision AI</i>",
            styles['Normal']
        ))
        
        # Build PDF
        doc.build(elements)
        print("[PDF] PDF report generated successfully")
        
        if output_path is None:
            buffer.seek(0)
            return buffer
        else:
            return output_path
    
    except Exception as e:
        print(f"[PDF] Error generating PDF report: {e}")
        import traceback
        traceback.print_exc()
        # Return empty buffer as fallback
        buffer = io.BytesIO()
        buffer.write(b'%PDF-1.4\nError generating report\n')
        buffer.seek(0)
        return buffer
