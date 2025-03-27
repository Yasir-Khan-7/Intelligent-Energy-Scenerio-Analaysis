import streamlit as st
from streamlit_folium import st_folium
import folium
import urllib.parse
import streamlit as st
import io
import os
import streamlit as st
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.utils import ImageReader

# Set page configuration
st.set_page_config(page_title="Contact Us", layout="wide")


# Load the logo (Update the path if needed)
LOGO_PATH = "images/iesa_green.png"  # Ensure this path is correct

# Function to create a custom PDF template
def create_pdf(actions):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4  # Get page size
    page_num = 1  # Start page number

    def draw_header_footer():
        header_y = height - 45  # Adjusted Top Border
        c.setStrokeColor(colors.HexColor("#4389a2"))
        c.setLineWidth(2)
        c.line(20, header_y, width - 20, header_y)

        c.setStrokeColor(colors.red)
        c.setLineWidth(2)
        c.line(20, 30, width - 20, 30)

        if os.path.exists(LOGO_PATH):
            logo = ImageReader(LOGO_PATH)
            logo_width, logo_height = 50, 20
            c.drawImage(logo, width - 70, height - 40, width=logo_width, height=logo_height, mask='auto')

    draw_header_footer()

    c.setFont("Helvetica-Bold", 18)
    title_text = "IESA Contact Us Report"
    title_width = c.stringWidth(title_text, "Helvetica-Bold", 18)
    c.drawString((width - title_width) / 2, height - 80, title_text)

    c.setFont("Helvetica", 12)

    y = height - 140  
    for action in actions:
        y -= 20
        if y < 70:
            c.setFont("Helvetica", 10)
            c.drawString(width - 50, 15, f"Page {page_num}")
            c.showPage()
            page_num += 1
            draw_header_footer()
            c.setFont("Helvetica", 12)
            y = height - 50
            c.setFont("Helvetica-Bold", 14)
            c.drawString(40, y, "Activity Log (cont.):")
            y -= 20
        
        c.setFont("Helvetica", 12)
        c.drawString(60, y, f" {action}")
         #Ensure action is properly formatted as multiline key-value pairs
        
    c.setFont("Helvetica-Oblique", 10)
    c.setFillColor(colors.gray)
    c.drawString(40, 15, "© 2025 IESA. All rights reserved.")
    c.setFillColor(colors.black)
    c.drawString(width - 50, 15, f"Page {page_num}")

    c.save()
    buffer.seek(0)
    return buffer

# Reset session state on page reload
if not st.session_state.get("initialized", False):
    st.session_state.user_actions = []
    st.session_state.initialized = True


#create a head tag to include font awesome icons
st.markdown(
    """
    <head>
        <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css" rel="stylesheet">
    </head>
    """,
    unsafe_allow_html=True,
)
# Custom CSS for styling with your gradient color updates
st.markdown(
    """
    <style>
    .stApp {
        margin-top: -70px !important; /* Adjust the top margin */
    }

    /* Contact Us section */
    div[data-testid="stColumn"]:first-child {
        padding: 40px;
        margin-right: -15px;
        border-top: 2px solid #cccccc;
        border-left: 2px solid #cccccc;
        border-bottom: 2px solid #cccccc;
        border-radius: 10px;
        background: white; /* White background for the form */
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1); /* Add subtle shadow for depth */
    }

    /* Gradient for form, button, and header borders */
    div[data-testid="stColumn"]:first-child .stTextInput > div, 
    div[data-testid="stColumn"]:first-child .stTextArea > div {
        border: 1px solid #cccccc; /* Updated borders */
        border-radius: 5px;
        padding: 4px; /* Add some padding */
        background-color: #f9f9f9; /* Light background for input fields */
    }

    /* Focus state for inputs */
    div[data-testid="stColumn"]:first-child .stTextInput > div:focus-within, 
    div[data-testid="stColumn"]:first-child .stTextArea > div:focus-within {
        border: 2px solid #4AC29A !important; /* Highlight on focus */
        box-shadow: 0 0 5px rgba(74, 194, 154, 0.3);
    }

    .stTextInput {
        width: 80%;
        margin-bottom: 15px !important; /* Increase spacing between fields */
       
    }

    .stTextArea {
        width: 80% !important;
        margin-bottom: 15px !important; /* Increase spacing between fields */
    }

    /* Placeholder text */
    .stTextInput input::placeholder, .stTextArea textarea::placeholder {
        color: black !important; /* Darker placeholder text for better visibility */
        font-weight: 400;
    }

    /* Button styling */
    div[data-testid="stButton"] > button {
        width: 80%;
        background-color: #4AC29A;
        color: white;
        font-size: 16px;
        font-weight: bold;
        border: none;
        border-radius: 5px;
        padding: 12px; /* Slightly larger button */
        cursor: pointer;
        transition: all 0.2s ease-in-out;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); /* Button shadow */
        margin-top: 10px;
    }

    div[data-testid="stButton"] > button:hover {
      background-color: #44A08D;
      color: white;
      transform: translateY(-2px);
      box-shadow: 0 6px 8px rgba(0, 0, 0, 0.15);
    }

    /* Map column with black gradient background */
    div[data-testid="stColumn"]:nth-child(2) {
        padding: 40px;
        background: linear-gradient(135deg, #232526, #414345); /* Improved contrast gradient */
        color: white; /* White text in the map column */
        border-radius: 10px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2); /* Add shadow for depth */
    }

    /* Heading and text styles for map column */
    div[data-testid="stColumn"]:nth-child(2) h2 {
        font-size: 28px;
        font-weight: bold;
        color: white;
        margin-bottom: 20px;
        border-bottom: 2px solid #4AC29A;
        padding-bottom: 10px;
        text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.3); /* Text shadow for better readability */
    }

    div[data-testid="stColumn"]:nth-child(2) p {
        font-size: 18px;
        color: #f0f0f0 !important; /* Brighter text color */
        margin-bottom: 15px;
        line-height: 1.6;
    }

    /* Target specific image styling in map column */
    div[data-testid="stColumn"]:nth-child(2) img {
        border: 3px solid #4AC29A; /* Thicker border around the map */
        border-radius: 10px;
        width: 100%; /* Set image width */
        margin-top: 20px;
    }

    /* Header Styling */
    header {
        border-bottom: 3px solid #4AC29A !important; /* Updated border for header */
        height: 50px !important;
    }

    /* Text styling */
    h1 {
        font-size: 38px;
        margin-bottom: 16px;
        font-weight: bold;
        color: #0F403F; /* Darker text for better contrast */
        text-shadow: 1px 1px 0px rgba(255, 255, 255, 0.5);
    }

    h5 {
        font-size: 20px;
        margin-bottom: 12px;
        color: #333333;
    }
    
    .required-fields {
        font-size: 16px;
        margin-bottom: 20px;
        color: #666666; /* Darker grey for better visibility */
        font-style: italic;
    }

    /* Hide the tooltip "Press Ctrl+Enter to apply" */
    [data-testid="InputInstructions"] {
        display: None;
    }
    
    iframe {
        border: 4px solid #4AC29A;
        border-radius: 10px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
    }
    
    /* Contact Icons */
    .contact-icon {
        font-size: 22px;
        margin-right: 15px;
        width: 30px;
        display: inline-block;
        text-align: center;
    }
    
    /* CSS for success and error messages */
    .custom-success {
        background-color: #0b8793;  /* Application primary greenish-blue */
        color: #FFFFFF;
        padding: 15px;
        border-radius: 5px;
        margin: 15px 0;
        width: 80%;
        font-size: 16px;
        font-weight: bold;
        box-shadow: 0 4px 6px rgba(11, 135, 147, 0.2); /* Subtle shadow */
        border-left: 5px solid #066570; /* Left border for emphasis */
    }
    
    /* Custom error message styling */
    .custom-error {
        background-color: #FF6B6B;  /* Soft red with some muted tone to match style */
        color: #FFFFFF;
        padding: 15px;
        border-radius: 5px;
        margin: 15px 0;
        width: 80%;
        font-size: 16px;
        font-weight: bold;
        box-shadow: 0 4px 6px rgba(255, 107, 107, 0.2); /* Soft shadow */
        border-left: 5px solid #E84C4C; /* Left border for emphasis */
    }

    [data-testid="stBaseButton-secondary"] {
        background-color: #44A08D;
        color: white;
        border-radius: 5px;
        padding: 8px 16px;
        font-weight: bold;
        border: none;
        transition: all 0.2s ease;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    [data-testid="stBaseButton-secondary"]:hover {
        background-color: #4AC29A;
        transform: translateY(-2px);
        box-shadow: 0 6px 8px rgba(0, 0, 0, 0.15);
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Layout: Using separate columns for the form and contact info
col1, col2 = st.columns([1, 1])  # Both columns will have equal width

with col1:
    # Content for the contact form
    st.image("images/iesa_green.svg", width=130)
    st.markdown("<h1>Contact Us</h1>", unsafe_allow_html=True)
    st.markdown("<h5>We would love to hear from you.</h5>", unsafe_allow_html=True)
    st.markdown(
        "<div class='required-fields'>Please fill out the form below to get in touch.</div>",
        unsafe_allow_html=True,
    )

    # Input fields for the contact form
    name = st.text_input("", placeholder="Your Name *")

    if name:  # Ensure name is not empty
        formatted_name = f"Name: {name}"
        if formatted_name not in st.session_state.user_actions:
            st.session_state.user_actions.append(formatted_name)

    email = st.text_input("", placeholder="Your Email *")
    
    if email:  # Ensure name is not empty
        formatted_email = f"Email: {email}"
        if formatted_email not in st.session_state.user_actions:
            st.session_state.user_actions.append(formatted_email)  

    message = st.text_area("", placeholder="Your Message *", height=150)

    if message:  # Ensure name is not empty
        formatted_message = f"Message: {message}"
        if formatted_message not in st.session_state.user_actions:
            st.session_state.user_actions.append(formatted_message)  

       
    # Send message button
    if st.button("Send Message"):
        if not name or not email or not message:
           st.markdown(
                "<div class='custom-error'>⚠️ Please fill all the required fields</div>",
                unsafe_allow_html=True,
            )
        else:
            # Prepare the Gmail draft link
            recipient = "nexzonsolutions@gmail.com"
            subject = f"Message from {name}"
            body = f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}"

            # Encode the mailto link
            gmail_draft_link = f"https://mail.google.com/mail/?view=cm&fs=1&to={recipient}&su={urllib.parse.quote(subject)}&body={urllib.parse.quote(body)}"

            # Use st.components.v1.html to trigger the link in a new tab
            st.components.v1.html(
                f'<script>window.open("{gmail_draft_link}", "_black");</script>',
                height=0,
                width=0,
                )
            st.markdown(
                    "<div class='custom-success'>✅ Gmail draft has been opened in a new tab!</div>",
                    unsafe_allow_html=True,
                )
            
            
with col2:
    # Contact information and map/image
    st.markdown("<h2>Reach Us Out</h2>", unsafe_allow_html=True)
    st.markdown(
    """
    <p><span class='contact-icon' style='color:#FF6B6B;'><i class="fa fa-envelope"></i></span>nexzonsolutions@gmail.com</p>
    <p><span class='contact-icon' style='color:#4AC29A;'><i class="fa fa-phone"></i></span> 051-5151437-38</p>
    <p><span class='contact-icon' style='color:#1E90FF;'><i class="fa fa-map-marker"></i></span>Foundation University Rawalpindi Campus</p>
    """,
    unsafe_allow_html=True,
    )
    
    # Add a map using folium
    map_center = [33.56118645224043, 73.07151744232765]  
    m = folium.Map(location=map_center, zoom_start=17)
    folium.Marker(
        location=map_center,
        popup="Your Location",
        icon=folium.Icon(color="blue", icon="info-sign"),
    ).add_to(m)
    st_folium(m, width=700, height=300)






if st.session_state.user_actions:
    pdf_buffer = create_pdf(st.session_state.user_actions)
    # Provide Download Button
    st.download_button("Download Report", pdf_buffer, "IESA_Report.pdf", "application/pdf")
    