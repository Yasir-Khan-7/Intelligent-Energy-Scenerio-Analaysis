import streamlit as st
from reportlab.lib.pagesizes import A4, portrait
from reportlab.pdfgen import canvas
from reportlab.lib import colors
import io
import base64
from datetime import datetime

# Function to create a minimalist cover page with simple IESA text and "Report"
def create_minimalist_cover():
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=portrait(A4))
    width, height = portrait(A4)  # Get page size
    
    # Draw white background
    c.setFillColor(colors.white)
    c.rect(0, 0, width, height, fill=1, stroke=0)
    
    # Draw top horizontal line (blue)
    c.setStrokeColor(colors.HexColor("#0055A4"))
    c.setLineWidth(2)
    c.line(10, height-20, width-10, height-20)
    
    # Draw bottom horizontal line (red)
    c.setStrokeColor(colors.red)
    c.setLineWidth(2)
    c.line(10, 20, width-10, 20)
    
    # Simple IESA text - just plain text with no styling
    c.setFillColor(colors.HexColor("#00A67E"))  # Green color
    c.setFont("Helvetica-Bold", 60)
    
    # Center the text
    iesa_text = "IESA"
    text_width = c.stringWidth(iesa_text, "Helvetica-Bold", 60)
    text_x = (width - text_width) / 2
    text_y = height/2 + 30
    
    # Draw the plain text
    c.drawString(text_x, text_y, iesa_text)
    
    # Add "REPORT" text below - with more style
    # Position it closer to IESA text
    report_y = text_y - 60  # Closer to IESA text
    
    # Add a subtle underline for REPORT text
    report_text = "REPORT"
    c.setFont("Helvetica-Bold", 38)  # Slightly larger
    c.setFillColor(colors.HexColor("#222222"))  # Darker for more contrast
    report_width = c.stringWidth(report_text, "Helvetica-Bold", 38)
    report_x = (width - report_width) / 2
    
    # Draw REPORT text
    c.drawString(report_x, report_y, report_text)
    
    # Add decorative underline
    c.setStrokeColor(colors.HexColor("#222222"))
    c.setLineWidth(1.5)
    c.line(report_x, report_y - 8, report_x + report_width, report_y - 8)
    
    # Add small decorative elements on sides of REPORT
    c.setFillColor(colors.HexColor("#222222"))
    c.circle(report_x - 15, report_y - 4, 3, fill=1, stroke=0)
    c.circle(report_x + report_width + 15, report_y - 4, 3, fill=1, stroke=0)
    
    # Add current date at the bottom
    c.setFont("Helvetica", 10)
    c.setFillColor(colors.HexColor("#666666"))
    current_date = datetime.now().strftime("%B %d, %Y")
    c.drawCentredString(width/2, 40, current_date)
    
    c.save()
    buffer.seek(0)
    return buffer

# Function to display PDF preview in Streamlit
def display_pdf(pdf_bytes):
    base64_pdf = base64.b64encode(pdf_bytes.read()).decode("utf-8")
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="700" height="500" type="application/pdf"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)

# Streamlit UI
st.title("IESA Cover Page Generator")

# Generate button
if st.button("Generate Minimalist Cover Page"):
    pdf_buffer = create_minimalist_cover()
    
    # Display PDF Preview
    st.subheader("📄 Cover Page Preview:")
    display_pdf(pdf_buffer)
    
    # Provide Download Button
    st.download_button("📥 Download Cover Page", pdf_buffer, "IESA_Cover.pdf", "application/pdf")