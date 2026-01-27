"""
PDF Report Generation.

WHAT: Functions to generate PDF reports with charts and statistics.
WHY: Users need downloadable reports of their equipment data.
HOW: Use ReportLab to create PDFs with tables, text, and charts.
"""

import io
import json
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.graphics.charts.piecharts import Pie
from django.http import HttpResponse
from .models import Dataset


def generate_pdf_report(dataset: Dataset) -> HttpResponse:
    """
    Generate a PDF report for a dataset.
    
    Args:
        dataset: Dataset instance to generate report for
    
    Returns:
        HttpResponse with PDF file
    
    Example:
        return generate_pdf_report(dataset)
    """
    # Create a file-like buffer to receive PDF data
    buffer = io.BytesIO()
    
    # Create the PDF object, using the buffer as its "file"
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    
    # Container for the 'Flowable' objects
    elements = []
    
    # Define styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#1e40af'),
        spaceAfter=30,
        alignment=1  # Center
    )
    heading_style = styles['Heading2']
    normal_style = styles['Normal']
    
    # Title
    title = Paragraph("Equipment Data Analysis Report", title_style)
    elements.append(title)
    elements.append(Spacer(1, 12))
    
    # Dataset Information
    info_heading = Paragraph("Dataset Information", heading_style)
    elements.append(info_heading)
    elements.append(Spacer(1, 6))
    
    info_data = [
        ['Dataset ID:', str(dataset.id)],
        ['Uploaded By:', dataset.user.username],
        ['Upload Date:', dataset.uploaded_at.strftime('%Y-%m-%d %H:%M:%S')],
        ['Total Equipment:', str(dataset.total_equipment)],
    ]
    
    info_table = Table(info_data, colWidths=[2*inch, 4*inch])
    info_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#e5e7eb')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
    ]))
    
    elements.append(info_table)
    elements.append(Spacer(1, 20))
    
    # Summary Statistics
    stats_heading = Paragraph("Summary Statistics", heading_style)
    elements.append(stats_heading)
    elements.append(Spacer(1, 6))
    
    stats_data = [
        ['Metric', 'Average Value'],
        ['Flowrate', f'{dataset.avg_flowrate:.2f}'],
        ['Pressure', f'{dataset.avg_pressure:.2f}'],
        ['Temperature', f'{dataset.avg_temperature:.2f}'],
    ]
    
    stats_table = Table(stats_data, colWidths=[3*inch, 3*inch])
    stats_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3b82f6')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f3f4f6')]),
    ]))
    
    elements.append(stats_table)
    elements.append(Spacer(1, 20))
    
    # Equipment Type Distribution
    types_heading = Paragraph("Equipment Type Distribution", heading_style)
    elements.append(types_heading)
    elements.append(Spacer(1, 6))
    
    try:
        types_dict = json.loads(dataset.equipment_types)
        types_data = [['Equipment Type', 'Count']]
        for eq_type, count in types_dict.items():
            types_data.append([eq_type, str(count)])
        
        types_table = Table(types_data, colWidths=[3*inch, 3*inch])
        types_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#10b981')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
            ('TOPPADDING', (0, 0), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f3f4f6')]),
        ]))
        
        elements.append(types_table)
        elements.append(Spacer(1, 20))
        
        # Add bar chart for equipment types
        if types_dict:
            drawing = Drawing(400, 200)
            chart = VerticalBarChart()
            chart.x = 50
            chart.y = 50
            chart.height = 125
            chart.width = 300
            chart.data = [list(types_dict.values())]
            chart.categoryAxis.categoryNames = list(types_dict.keys())
            chart.valueAxis.valueMin = 0
            chart.bars[0].fillColor = colors.HexColor('#3b82f6')
            
            drawing.add(chart)
            elements.append(drawing)
            elements.append(Spacer(1, 20))
    
    except:
        pass
    
    # Equipment Details Table (first 10 records)
    details_heading = Paragraph("Equipment Details (Sample)", heading_style)
    elements.append(details_heading)
    elements.append(Spacer(1, 6))
    
    equipment_records = dataset.equipment_records.all()[:10]
    
    details_data = [['Name', 'Type', 'Flowrate', 'Pressure', 'Temp']]
    for record in equipment_records:
        details_data.append([
            record.equipment_name[:20],  # Truncate long names
            record.equipment_type[:15],
            f'{record.flowrate:.1f}',
            f'{record.pressure:.1f}',
            f'{record.temperature:.1f}'
        ])
    
    details_table = Table(details_data, colWidths=[1.8*inch, 1.3*inch, 1*inch, 1*inch, 1*inch])
    details_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#6366f1')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f3f4f6')]),
    ]))
    
    elements.append(details_table)
    
    # Add footer note
    elements.append(Spacer(1, 20))
    footer_text = f"Generated on {dataset.uploaded_at.strftime('%Y-%m-%d %H:%M:%S')} | Total Records: {dataset.total_equipment}"
    footer = Paragraph(footer_text, normal_style)
    elements.append(footer)
    
    # Build PDF
    doc.build(elements)
    
    # Get the value of the BytesIO buffer and write it to the response
    pdf = buffer.getvalue()
    buffer.close()
    
    # Create the HttpResponse object with PDF headers
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="equipment_report_{dataset.id}.pdf"'
    response.write(pdf)
    
    return response
