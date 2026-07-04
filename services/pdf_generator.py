from fpdf import FPDF
import os
import uuid

class ReportPDF(FPDF):
    def header(self):
        self.set_font('helvetica', 'B', 15)
        self.cell(0, 10, 'AI Company Research Report', border=False, ln=1, align='C')
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font('helvetica', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}/{{nb}}', align='C')

    def section_title(self, title):
        self.set_font('helvetica', 'B', 12)
        self.set_fill_color(200, 220, 255)
        self.cell(0, 8, title, ln=1, fill=True)
        self.ln(2)

    def section_body(self, text):
        self.set_font('helvetica', '', 10)
        self.multi_cell(0, 5, text)
        self.ln(5)

def generate_pdf(data):
    """Generates a PDF from the report data and returns the file path."""
    pdf = ReportPDF()
    pdf.alias_nb_pages()
    pdf.add_page()

    # Company Info
    pdf.set_font('helvetica', 'B', 14)
    pdf.cell(0, 10, data.get('companyName', 'Unknown Company'), ln=1)
    
    pdf.set_font('helvetica', '', 10)
    pdf.cell(0, 6, f"Website: {data.get('website', 'N/A')}", ln=1)
    pdf.cell(0, 6, f"Phone: {data.get('phoneNumber', 'N/A')}", ln=1)
    pdf.cell(0, 6, f"Address: {data.get('address', 'N/A')}", ln=1)
    pdf.ln(5)

    # Products / Services
    pdf.section_title("Products / Services")
    pdf.section_body(data.get('productsServices', 'N/A'))

    # Pain Points
    pdf.section_title("AI-Generated Pain Points")
    pdf.section_body(data.get('painPoints', 'N/A'))

    # Competitors
    pdf.section_title("Competitor Information")
    competitors = data.get('competitors', [])
    if competitors:
        for comp in competitors:
            pdf.set_font('helvetica', 'B', 10)
            pdf.cell(0, 5, f"- {comp.get('name', 'N/A')}", ln=1)
            pdf.set_font('helvetica', 'U', 10)
            pdf.set_text_color(0, 0, 255)
            pdf.cell(0, 5, f"  {comp.get('website', 'N/A')}", ln=1, link=comp.get('website', ''))
            pdf.set_text_color(0, 0, 0)
    else:
        pdf.section_body("No competitors found.")

    os.makedirs('tmp', exist_ok=True)
    filename = f"report_{uuid.uuid4().hex}.pdf"
    filepath = os.path.join('tmp', filename)
    pdf.output(filepath)
    
    return filepath
