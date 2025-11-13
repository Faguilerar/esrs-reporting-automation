"""
Report Generator Module
Generates PDF reports from processed ESRS data
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors
from datetime import datetime
import yaml
import os

class ESRSReportGenerator:
    def __init__(self, config_path='config/config.yaml'):
        """Initialize report generator"""
        with open(config_path, 'r') as file:
            self.config = yaml.safe_load(file)
        
        self.company_name = self.config['report']['company_name']
        self.reporting_period = self.config['report']['reporting_period']
        self.styles = getSampleStyleSheet()
        
        # Custom styles
        self.title_style = ParagraphStyle(
            'CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=self.config['pdf']['title_font_size'],
            textColor=colors.HexColor('#1f4788'),
            spaceAfter=30,
            alignment=1  # Center
        )
        
        self.heading_style = ParagraphStyle(
            'CustomHeading',
            parent=self.styles['Heading2'],
            fontSize=self.config['pdf']['heading_font_size'],
            textColor=colors.HexColor('#2e5c8a'),
            spaceAfter=12,
            spaceBefore=12
        )
    
    def create_cover_page(self):
        """Create report cover page"""
        elements = []
        
        # Title
        title = Paragraph(
            f"<b>ESRS Sustainability Report</b>",
            self.title_style
        )
        elements.append(Spacer(1, 3*cm))
        elements.append(title)
        elements.append(Spacer(1, 1*cm))
        
        # Company and period
        company_info = Paragraph(
            f"<b>{self.company_name}</b><br/>"
            f"Reporting Period: {self.reporting_period}",
            self.styles['Normal']
        )
        elements.append(company_info)
        elements.append(Spacer(1, 2*cm))
        
        # Generation date
        date_text = Paragraph(
            f"Generated on: {datetime.now().strftime('%B %d, %Y')}",
            self.styles['Normal']
        )
        elements.append(date_text)
        elements.append(PageBreak())
        
        return elements
    
    def create_executive_summary(self, metrics):
        """Create executive summary section"""
        elements = []
        
        elements.append(Paragraph("<b>Executive Summary</b>", self.title_style))
        elements.append(Spacer(1, 0.5*cm))
        
        summary_text = f"""
        This report presents the sustainability performance of {self.company_name} 
        for the period {self.reporting_period} in accordance with the European 
        Sustainability Reporting Standards (ESRS).
        """
        elements.append(Paragraph(summary_text, self.styles['Normal']))
        elements.append(Spacer(1, 1*cm))
        
        return elements
    
    def create_module_section(self, module, metrics):
        """Create section for each ESRS module"""
        elements = []
        
        # Module titles
        module_titles = {
            'E1': 'E1 - Climate Change',
            'E2': 'E2 - Pollution',
            'E3': 'E3 - Water and Marine Resources',
            'E4': 'E4 - Biodiversity and Ecosystems',
            'E5': 'E5 - Resource Use and Circular Economy',
            'S1': 'S1 - Own Workforce',
            'S2': 'S2 - Workers in the Value Chain',
            'S3': 'S3 - Affected Communities',
            'S4': 'S4 - Consumers and End-users',
            'G1': 'G1 - Business Conduct'
        }
        
        # Section title
        title = module_titles.get(module, module)
        elements.append(Paragraph(f"<b>{title}</b>", self.heading_style))
        elements.append(Spacer(1, 0.3*cm))
        
        # Create table with metrics
        if metrics:
            table_data = [['Metric', 'Value']]
            
            for key, value in metrics.items():
                metric_name = key.replace('_', ' ').title()
                
                # Format value
                if isinstance(value, float):
                    formatted_value = f"{value:,.2f}"
                else:
                    formatted_value = str(value)
                
                table_data.append([metric_name, formatted_value])
            
            # Create table
            table = Table(table_data, colWidths=[10*cm, 5*cm])
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2e5c8a')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 1), (-1, -1), 10),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), 
                 [colors.white, colors.HexColor('#f0f0f0')])
            ]))
            
            elements.append(table)
        else:
            elements.append(Paragraph("No data available for this module.", 
                                    self.styles['Normal']))
        
        elements.append(Spacer(1, 1*cm))
        
        return elements
    
    def generate_report(self, all_metrics):
        """Generate complete PDF report"""
        # Create output folder
        output_folder = self.config['report']['output_folder']
        os.makedirs(output_folder, exist_ok=True)
        
        # Generate filename
        date_str = datetime.now().strftime('%Y%m%d')
        filename = self.config['report']['output_filename'].replace('{date}', date_str)
        output_path = os.path.join(output_folder, filename)
        
        # Create PDF
        doc = SimpleDocTemplate(output_path, pagesize=A4)
        elements = []
        
        # Add cover page
        elements.extend(self.create_cover_page())
        
        # Add executive summary
        elements.extend(self.create_executive_summary(all_metrics))
        elements.append(PageBreak())
        
        # Add sections for each module
        for module in self.config['esrs_modules']:
            if module in all_metrics and all_metrics[module]:
                elements.extend(self.create_module_section(module, 
                                                          all_metrics[module]))
        
        # Build PDF
        doc.build(elements)
        print(f"\nReport generated successfully: {output_path}")
        
        return output_path

if __name__ == "__main__":
    # Test report generator
    generator = ESRSReportGenerator()
    
    # Sample metrics for testing
    test_metrics = {
        'E1': {'total_emissions': 12500.50, 'total_scope1': 5000.25},
        'E2': {'total_air_pollutants': 150.75}
    }
    
    generator.generate_report(test_metrics)
  
