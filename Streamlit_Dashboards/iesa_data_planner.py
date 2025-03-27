import mysql.connector
import pandas as pd
import streamlit as st
import os
import altair as alt
import locale
import io
import os
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import Image
from reportlab.lib.utils import ImageReader

# Initialize sidebar state and button text
if 'sidebar_state' not in st.session_state:
    st.session_state.sidebar_state = 'expanded'
if 'button_text' not in st.session_state:
    st.session_state.button_text = '← Hide'
if 'needs_rerun' not in st.session_state:
    st.session_state.needs_rerun = False

# Function to toggle sidebar
def toggle_sidebar():
    if st.session_state.sidebar_state == 'expanded':
        st.session_state.sidebar_state = 'collapsed'
        st.session_state.button_text = '→ Show'
    else:
        st.session_state.sidebar_state = 'expanded'
        st.session_state.button_text = '← Hide'
    st.session_state.needs_rerun = True

# Function to auto-hide sidebar
def hide_sidebar():
    st.session_state.sidebar_state = 'collapsed'
    st.session_state.button_text = '→ Show'
    st.session_state.needs_rerun = True

st.set_page_config(page_title="IESA Dashboard", layout="wide", page_icon="📊", initial_sidebar_state=st.session_state.sidebar_state)


# Load logo
LOGO_PATH = "images/iesa_green.png"  # Update path if needed

# Session state for user actions
if "user_actions" not in st.session_state:
    st.session_state.user_actions = []

if "chart_paths" not in st.session_state:
    st.session_state.chart_paths = []

def add_chart(chart_path):
    if chart_path not in st.session_state.chart_paths:
        st.session_state.chart_paths.append(chart_path)

# Function to create PDF
def create_pdf(chart_paths):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    page_num = 1

    def draw_header_footer():
        header_y = height - 45
        c.setStrokeColor(colors.HexColor("#4389a2"))
        c.setLineWidth(2)
        c.line(20, header_y, width - 20, header_y)
        c.setStrokeColor(colors.red)
        c.setLineWidth(2)
        c.line(20, 30, width - 20, 30)
        if os.path.exists(LOGO_PATH):
            logo = ImageReader(LOGO_PATH)
            c.drawImage(logo, width - 70, height - 40, width=50, height=20, mask='auto')

    draw_header_footer()

    c.setFillColor(colors.HexColor("#504B38")) 
    c.setFont("Helvetica-Bold", 18)
    title_text = "Data Planner Report"
    c.drawString((width - c.stringWidth(title_text, "Helvetica-Bold", 18)) / 2, height - 80, title_text)
    c.setFont("Helvetica", 12)

    y = height - 120
    # for action in actions:
    #     y -= 20
    #     if y < 70:
    #         c.setFont("Helvetica", 10)
    #         c.drawString(width - 50, 15, f"Page {page_num}")
    #         c.showPage()
    #         page_num += 1
    #         draw_header_footer()
    #         c.setFont("Helvetica", 12)
    #         y = height - 50
    #         c.setFont("Helvetica-Bold", 14)
    #         c.drawString(40, y, "Activity Log (cont.):")
    #         y -= 20
        
    #     c.setFont("Helvetica", 12)
    #     c.drawString(60, y, f" {action}")
         #Ensure action is properly formatted as multiline key-value pairs
     # Add chart to PDF on the same page if space allows
   # Add multiple charts to PDF
    # Add only the latest charts
    x_left = 50
    column_margin = 15  # Extra spacing between columns
    x_right = (width / 2) + column_margin  # Adjusted for margin
    chart_width = 250
    chart_height = 200
    padding = 1.9  # Padding around the image
    border_radius = 5  # Rounded corners

    column = 0
    border_color = (11/255, 135/255, 147/255)  # RGB conversion of #0b8793

    for chart_path in chart_paths:
        if os.path.exists(chart_path):
            if y - chart_height > 30:
                x_pos = x_left if column % 2 == 0 else x_right

                # Adjusted position for padding
                border_x = x_pos - padding
                border_y = y - chart_height - padding
                border_width = chart_width + (2 * padding)
                border_height = chart_height + (2 * padding)

                # Draw the rounded rectangle border
                c.setStrokeColorRGB(*border_color)
                c.setLineWidth(1)
                c.roundRect(border_x, border_y, border_width, border_height, border_radius, stroke=1, fill=0)

                # Draw the image
                c.drawImage(chart_path, x_pos, y - chart_height, width=chart_width, height=chart_height, mask='auto')

                if column % 2 == 1:
                    y -= chart_height + 20  # Move down after placing two charts
                column += 1
            else:
                c.showPage()
                page_num += 1
                draw_header_footer()
                y = height - 100
                x_pos = x_left

                # Adjusted position for padding
                border_x = x_pos - padding
                border_y = y - chart_height - padding

                # Draw the rounded rectangle border
                c.setStrokeColorRGB(*border_color)
                c.setLineWidth(1)
                c.roundRect(border_x, border_y, border_width, border_height, border_radius, stroke=1, fill=0)

                # Draw the image
                c.drawImage(chart_path, x_pos, y - chart_height, width=chart_width, height=chart_height, mask='auto')

                column = 1  # Reset to first column on new page
    c.setFont("Helvetica-Oblique", 10)
    c.setFillColor(colors.gray)
    c.drawString(40, 15, "© 2025 IESA. All rights reserved.")
    c.setFillColor(colors.black)
    c.drawString(width - 50, 15, f"Page {page_num}")
    
    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer

# Function to format large numbers
def format_large_number(num):
    if num >= 1_000_000:
        return f"{locale.format_string('%d', num // 1_000_000)} million"
    elif num >= 1_000:
        return f"{locale.format_string('%d', num // 1_000)} thousand"
    return locale.format_string('%d', num)

# Connection
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        port="3306",
        user="root",
        passwd="admin123",
        db="iesa_db"
    )

# Function to fetch tables from the database
def fetch_tables():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SHOW TABLES")
        tables = [table[0] for table in cursor.fetchall()]
        conn.close()
        return tables
    except Exception as e:
        print(f"Error fetching tables: {e}")
        return []

# Function to fetch data from a specific table
def fetch_table_data(table_name):
    conn = get_connection()
    cursor = conn.cursor()
    query = "SELECT * FROM {}".format(table_name)  # Still a risk
    cursor.execute(query)
    rows = cursor.fetchall()
    data = pd.DataFrame(rows, columns=[desc[0] for desc in cursor.description])
    conn.close()
    return data

# Local image path (Replace with your actual image path)
image_path = "images/iesa_white.svg"

# CSS and JavaScript for dynamic button states
st.markdown("""
    <style>
    /* General Styling */
    header {
        border-bottom: 3px solid  #136a8a !important; 
    }
    [data-testid="stSidebar"] {
        background: linear-gradient(135deg, #73C8A9, #0b8793); /* Gradient background */
        color: white;
        margin-top:58px;
        box-shadow: 2px 0 10px rgba(0,0,0,0.2);
    }
    .sidebar-content {
        margin-top: -60px;
        padding: 20px;
    }
    
    /* Toggle button specific styles - target the first button in the first column */
    div[data-testid="stHorizontalBlock"] > div:first-child .stButton button {
        background-color: #0b8793;
        color: white !important;
        border: 1px solid #4AC29A;
        border-radius: 5px;
        padding: 8px 15px;
        font-weight: bold;
        box-shadow: 0 2px 5px rgba(0,0,0,0.2);
        transition: all 0.3s ease;
        position: fixed;
        z-index: 999;
        width: auto !important;
        min-width: 80px;
        max-width: 100px;
        margin-top: 25px;
        margin-bottom: 20px;
    }

    div[data-testid="stHorizontalBlock"] > div:first-child .stButton button:hover {
        background-color: #4AC29A;
        transform: translateY(-1px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    
    /* Sidebar element styling */
    [data-testid="stSidebar"] h2 {
        font-size: 22px !important;
        margin-top: 25px !important;
        margin-bottom: 15px !important;
        padding-bottom: 5px;
        border-bottom: 2px solid rgba(255,255,255,0.3);
        text-shadow: 1px 1px 2px rgba(0,0,0,0.2);
    }
    
    [data-testid="stSidebar"] p, [data-testid="stSidebar"] label {
        color: rgba(255,255,255,0.9) !important;
        font-weight: 500;
        margin-bottom: 8px;
        font-size: 15px;
    }
    
    [data-testid="stSidebar"] .stSelectbox > div {
        background-color: rgba(255,255,255,0.1) !important;
        border: 1px solid rgba(255,255,255,0.2) !important;
        border-radius: 5px;
        color: white !important;
        margin-bottom: 15px;
    }
    
    [data-testid="stSidebar"] .stSelectbox > div:hover {
        border: 1px solid rgba(255,255,255,0.4) !important;
    }
    
    /* Link styling */
    a {
        text-decoration: none;
        color: #0F403F !important;
    }
    
    a:hover {
        color: #0F403F !important;
        text-decoration: none;
    }
    
    /* Sidebar specific button styles */
    [data-testid="stSidebar"] .stButton button {
        width: 100%;
        background-color: #0b8793;
        color: white !important;
        border: 1px solid #4AC29A;
        border-radius: 5px;
        font-size: 0.9em;
        font-weight: bold;
        padding: 8px 20px;
        cursor: pointer;
        transition: all 0.3s ease;
        margin-bottom: 10px;
        letter-spacing: 0.3px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }

    [data-testid="stSidebar"] .stButton button:hover {
        background-color: #4AC29A;
        color: white !important;
        box-shadow: 0 3px 7px rgba(0,0,0,0.15);
        transform: translateY(-1px);
    }
    
    /* Other sidebar specific elements */
    [data-testid="stSidebar"] [data-testid="stBaseButton-secondary"] {
        background-color: #0b8793 !important;
        width: 100% !important;
        border: 1px solid #4AC29A;
        border-radius: 5px;
    }

    [data-testid="stSidebar"] [data-testid="stBaseButton-secondary"]:hover {
        background-color: #0b8793;
        color: white !important;
    }

    /* Fix column layout */
    .row-widget.stHorizontalBlock {
        flex-wrap: wrap;
        gap: 20px;
    }
    
    /* Make sure columns take equal space - exactly 2 per row */
    [data-testid="column"] {
        width: calc(50% - 10px) !important;
        flex: 0 0 calc(50% - 10px) !important;
        max-width: calc(50% - 10px) !important;
        margin: 0 !important;
        padding: 0 !important;
    }
    
    /* Ensure charts take full width of their containers */
    .element-container {
        width: 100% !important;
    }
    
    /* Chart styling */
    .chart {
        width: 100%;
        border: 1px solid #e0e0e0;
        border-radius: 8px;
        padding: 10px;
        background: white;
        box-shadow: none;
    }
    
    /* Main content spacing */
    .block-container {
        padding-top: 30px !important;
        max-width: 95%;
        margin: 0 auto;
    }

    

    .sum-button, .count-button, .total-button, .unique-button {
        padding: 8px 15px;  /* Reduced padding */
        border-radius: 12px;  /* Slightly smaller border radius */
        text-align: center;
        margin: 5px;
        color: white;
        font-weight: bold;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
        border: none;
        width: 120px;  /* Set a fixed width for each button */
        font-size: 0.85em;  /* Reduced font size */
    }

    /* Greenish Gradient (matching sidebar) */
    .sum-button { 
        background: linear-gradient(135deg, #73C8A9, #0b8793);  /* Sidebar-like greenish tones */
    }

    /* Redish Gradient (lighter tones) */
    .count-button { 
        background: linear-gradient(135deg, #FF6F61, #DE4313);  /* Lighter red gradient */
    }

    /* Blueish Gradient (lighter tones) */
    .total-button { 
        background: linear-gradient(135deg, #56CCF2, #2F80ED);  /* Lighter blue gradient */
    }

    /* Soft Greenish Gradient for Unique Button */
    .unique-button { 
        background: linear-gradient(135deg, #A5D6A7, #66BB6A);  /* Soft green gradient */
    }

    /* Hover effects */
    .sum-button:hover, .count-button:hover, .total-button:hover, .unique-button:hover {
        transform: translateY(-5px);
        box-shadow: 0px 8px 15px rgba(0, 0, 0, 0.2);
    }
    
    .marks{
        border-radius: 15px; /* Rounded corners for the SVG canvas */
        border: 1px solid  #0b8793; /* Greenish border */
        box-shadow: none;
        margin-top: 30px;  /* Reduced from 40px */
        padding: 15px; /* Reduced from 20px */
        width: 99%; /* Full width */
    }

    /* Chart Improvements */
    .marks {
        border-radius: 15px;
        border: 1px solid #0b8793;
        box-shadow: none;
        margin-top: 30px;  /* Reduced from 40px */
        padding: 15px; /* Reduced from 20px */
        width: 99%;
        background-color: #f9fcfc;
    }
    
    /* Chart styling */
    .chart-wrapper {
        margin-bottom: 20px; /* Reduced from 30px */
        background: white;
        padding: 15px; /* Reduced from 20px */
        border-radius: 10px;
        box-shadow: none;
    }
    
    .marks .axis-title, .marks .axis-label {
        font-weight: bold !important;
        font-size: 16px !important;
        fill: #333 !important;
    }
    
    .marks .axis-domain, .marks .axis-tick {
        stroke: #333 !important;
        stroke-width: 2px !important;
    }
    
    .marks .mark-line line {
        stroke-width: 3.5px !important;
    }
    
    .marks .mark-point circle {
        stroke-width: 1.5px !important;
        fill-opacity: 1 !important;
    }
    </style>
""", unsafe_allow_html=True)

# Add the toggle button at the top with a narrower column
toggle_col1, toggle_col2 = st.columns([1, 11])
with toggle_col1:
    st.button(st.session_state.button_text, key="toggle_sidebar_button", on_click=toggle_sidebar)

# Initialize session state
if "charts" not in st.session_state:
    st.session_state["charts"] = []

if "metrics" not in st.session_state:
    st.session_state["metrics"] = []

if "selected_table" not in st.session_state:
    st.session_state["selected_table"] = None

# Add extra spacing to move the content down
st.markdown("<div style='margin-top: 60px;'></div>", unsafe_allow_html=True)

# Sidebar for table selection
st.sidebar.image(image_path,width=150)
st.sidebar.markdown("""
    <h2>Data Planner Dashboard</h2>
""",unsafe_allow_html=True)
st.sidebar.markdown("""
    <h3>Table and Chart Selection</h3>
""",unsafe_allow_html=True)

# Fetch tables and display table selection
tables = fetch_tables()
selected_table = st.sidebar.selectbox("Select a table", tables)

# Initialize session state for charts and metrics if not already done
if 'charts' not in st.session_state:
    st.session_state['charts'] = []  # Store charts from all tables
if 'metrics' not in st.session_state:
    st.session_state['metrics'] = []  # Store metrics from all tables

# Fetch data for the selected table
if selected_table:
    data = fetch_table_data(selected_table)
    columns = data.columns.tolist()

    # Chart selection
    st.sidebar.markdown("### Chart Options")
    chart_type = st.sidebar.selectbox("Select Chart Type", ["Bar", "Line"])
    x_axis = st.sidebar.selectbox("Select x-axis", columns, key="chart_x_axis")
    y_axis = st.sidebar.selectbox("Select y-axis", columns, key="chart_y_axis")
    
    # Add option to show values on charts
    show_values = st.sidebar.checkbox("Show values on chart", value=False, key="show_values")
    
    add_chart = st.sidebar.button("Add Chart", key="add_chart_button")

    # Metric selection
    st.sidebar.markdown("### Metric Options")
    metric_column = st.sidebar.selectbox("Select Column for Metric", columns, key="metric_column")
    metric_type = st.sidebar.selectbox("Select Metric Type", ["Sum", "Count", "Average", "Unique"])
    add_metric = st.sidebar.button("Add Metric", key="add_metric_button")

    reset_button = st.sidebar.button("Reset Dashboard")
    
    # Add charts to session state (retain charts from all tables)
    if add_chart:
        st.session_state["charts"].append((selected_table, chart_type, x_axis, y_axis, show_values))
        # Hide sidebar when chart is added
        hide_sidebar()

    # Add metrics to session state (retain metrics from all tables)
    if add_metric:
        st.session_state["metrics"].append((selected_table, metric_column, metric_type))
        # Hide sidebar when metric is added
        hide_sidebar()

    # Reset button functionality
    if reset_button:
        # Reset session state
        st.session_state["charts"] = []
        st.session_state["metrics"] = []
        st.session_state["selected_table"] = None

# Display metrics dynamically from all selected tables
if st.session_state["metrics"]:
    metric_buttons_html = '<div class="metric-buttons">'

    for metric in st.session_state["metrics"]:
        table, column, metric_type = metric
        metric_data = fetch_table_data(table)

        if metric_type == "Sum":
            result = int(metric_data[column].sum())
            formatted_result = format_large_number(result)
            button_class = "sum-button"
            metric_label = f"{column}:"
        elif metric_type == "Count":
            result = int(metric_data[column].count())
            formatted_result = format_large_number(result)
            button_class = "count-button"
            metric_label = f"{column}:"
        elif metric_type == "Average":
            result = int(metric_data[column].mean())
            formatted_result = format_large_number(result)
            button_class = "total-button"
            metric_label = f"{column}:"
        elif metric_type == "Unique":
            result = int(metric_data[column].nunique())
            formatted_result = format_large_number(result)
            button_class = "unique-button"
            metric_label = f"{column}:"

        metric_buttons_html += f'<button class="{button_class}">{metric_label} {formatted_result}</button>'

    metric_buttons_html += '</div>'
    st.markdown(metric_buttons_html, unsafe_allow_html=True)


# List of color schemes
color_schemes = ['blues', 'tealblues', 'teals', 'greens', 'browns', 'greys', 'purples', 'warmgreys', 'reds', 'oranges']

# Assuming chart_data, chart_type, x_axis, y_axis, chart_title, and num_cols are already defined

# Dropdown to select the color scheme
selected_color_scheme = st.sidebar.selectbox("Choose Color Scheme", color_schemes)
# Display charts dynamically from all selected tables
if st.session_state["charts"]:
    num_cols = 2  # Adjust number of columns if needed
    cols = st.columns(num_cols)

     # Clear previous chart paths before generating new ones
    st.session_state.chart_paths = []

    for idx, chart in enumerate(st.session_state["charts"]):
        table, chart_type, x_axis, y_axis = chart if len(chart) == 4 else chart[:4]
        show_values = chart[4] if len(chart) > 4 else False
        chart_data = fetch_table_data(table)  # Fetch data for the associated table

        chart_title = f"{table.replace('_', ' ').title()}: {x_axis} vs {y_axis}"
        
        with cols[idx % num_cols]:
            if chart_type == "Bar":
                # Create the base bar chart
                bar_chart = alt.Chart(chart_data).mark_bar().encode(
                    x=alt.X(
                        x_axis,
                        title=x_axis,
                        axis=alt.Axis(
                            labelAngle=0,
                            titleFontSize=16,
                            labelFontSize=14,
                            titleFontWeight='bold',
                            labelFontWeight='bold',
                            titleColor='#333333',
                            labelColor='#333333',
                            grid=True,
                            gridColor='#e0e0e0',
                            tickSize=6,
                            tickWidth=2
                        )
                    ),
                    y=alt.Y(
                        y_axis,
                        title=y_axis,
                        axis=alt.Axis(
                            titleFontSize=16,
                            labelFontSize=14,
                            titleFontWeight='bold',
                            labelFontWeight='bold',
                            titleColor='#333333',
                            labelColor='#333333',
                            grid=True,
                            gridColor='#e0e0e0',
                            tickSize=6,
                            tickWidth=2
                        )
                    ),
                    # Color gradient based on y-axis values (not x-axis) for better visualization of magnitude
                    color=alt.Color(
                        y_axis,
                        scale=alt.Scale(scheme=selected_color_scheme),
                        legend=None
                    ),
                    tooltip=[x_axis, alt.Tooltip(y_axis, format=',d')]  # Enhanced tooltip with formatted values
                )
                
                # If show_values is True, add value labels
                if show_values:
                    # Create a temporary field with the value divided by 1000
                    chart_data['display_value'] = (chart_data[y_axis] / 1000).astype(int)
                    
                    # Add value labels on top of bars
                    text = alt.Chart(chart_data).mark_text(
                        align='center',
                        baseline='middle',
                        dy=-14,  # Reduced position offset (was -18)
                        fontSize=16,  # Smaller font size (was 18)
                       
                        stroke='black',  # White outline
                        strokeWidth=1,  # Minimal outline thickness
                        strokeOpacity=0.3  # Very low opacity for the outline
                    ).encode(
                        x=alt.X(x_axis),
                        y=alt.Y(y_axis),
                        text='display_value:Q',  # Use the calculated display value
                        color=alt.value('#000000')  # Pure black for maximum contrast
                    )
                    chart = (bar_chart + text).properties(
                        title=chart_title,
                        width='container',
                        height=350 # Increased from 280
                    )
                else:
                    chart = bar_chart.properties(
                        title=chart_title,
                        width='container',
                        height=350 # Increased from 280
                    )
                
                # Apply common configuration
                chart = chart.configure_view(
                    strokeWidth=1,
                    stroke='#cccccc'
                ).configure_axis(
                    grid=True,
                    gridColor='#e6e6e6',
                    domainColor='#666666',
                    tickColor='#666666',
                    domainWidth=2,
                    tickWidth=2
                ).configure_title(
                    fontSize=18,
                    font='Arial',
                    anchor='middle',
                    color='#333333'
                )
                
            elif chart_type == "Line":
                chart = alt.Chart(chart_data).mark_line(
                    color='#0066cc',
                    strokeWidth=3
                ).encode(
                    x=alt.X(
                        x_axis,
                        title=x_axis,
                        axis=alt.Axis(
                            labelAngle=0,
                            titleFontSize=16,
                            labelFontSize=14,
                            titleFontWeight='bold',
                            labelFontWeight='bold',
                            titleColor='#333333',
                            labelColor='#333333',
                            grid=True,
                            gridColor='#e0e0e0',
                            tickSize=6,
                            tickWidth=2
                        )
                    ),
                    y=alt.Y(
                        y_axis,
                        title=y_axis,
                        axis=alt.Axis(
                            titleFontSize=16,
                            labelFontSize=14,
                            titleFontWeight='bold',
                            labelFontWeight='bold',
                            titleColor='#333333',
                            labelColor='#333333',
                            grid=True,
                            gridColor='#e0e0e0',
                            tickSize=6,
                            tickWidth=2
                        )
                    )
                ).properties(
                    title=chart_title,
                    width='container',
                    height=350 # Increased from 280
                ).configure_view(
                    strokeWidth=1,
                    stroke='#cccccc'
                ).configure_axis(
                    grid=True,
                    gridColor='#e6e6e6',
                    domainColor='#666666',
                    tickColor='#666666',
                    domainWidth=2,
                    tickWidth=2
                )

            st.altair_chart(chart, use_container_width=True)
            # Save chart as image
           # When generating a new chart, clear previous chart paths
        
            chart_folder = "chart_images"
            os.makedirs(chart_folder, exist_ok=True)  # Create the folder if it doesn't exist


            chart_path = os.path.join(chart_folder, f"chart_{len(st.session_state.chart_paths) + 1}.png")
            chart.save(chart_path)

            
            st.session_state.chart_paths.append(chart_path)
            
# Streamlit interaction
if selected_table:
    if st.sidebar.button("Logout", key="logout_button"):
        os.system("streamlit run iesa_login.py")

    if st.sidebar.button("Contact Us", key="contact_us_button"):
        os.system("streamlit run iesa_contact_us.py")

        # Generate and provide PDF download

    
if  st.session_state.chart_paths:
    pdf_buffer = create_pdf(st.session_state.chart_paths)
    st.sidebar.download_button("Download Report", pdf_buffer, "IESA_Report.pdf", "application/pdf")

# Check if we need to rerun the script
if st.session_state.needs_rerun:
    st.session_state.needs_rerun = False
    st.rerun()