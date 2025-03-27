import streamlit as st
import pandas as pd
import mysql.connector
import groq
import altair as alt
from smolagents import Tool

# Initialize sidebar state
if 'sidebar_state' not in st.session_state:
    st.session_state.sidebar_state = 'expanded'
if 'button_text' not in st.session_state:
    st.session_state.button_text = '← Hide'
if 'previous_scenarios' not in st.session_state:
    st.session_state.previous_scenarios = []
if 'should_rerun' not in st.session_state:
    st.session_state.should_rerun = False

# Function to toggle sidebar
def toggle_sidebar():
    if st.session_state.sidebar_state == 'expanded':
        st.session_state.sidebar_state = 'collapsed'
        st.session_state.button_text = '→ Show'
    else:
        st.session_state.sidebar_state = 'expanded'
        st.session_state.button_text = '← Hide'
    st.session_state.should_rerun = True

# Function to auto-hide sidebar
def auto_hide_sidebar():
    st.session_state.sidebar_state = 'collapsed'
    st.session_state.button_text = '→ Show'
    st.session_state.should_rerun = True

# Set page config with initial sidebar state
st.set_page_config(
    page_title="IESA Scenario Analysis", 
    layout="wide", 
    page_icon="📊",
    initial_sidebar_state=st.session_state.sidebar_state
)

# Database connection
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        port="3306",
        user="root",
        passwd="admin123",
        db="iesa_db"
    )

# Fetch Scenarios from Database
def fetch_scenarios():
    conn = get_connection()
    query = "SELECT category, scenario FROM scenario_definitions;"
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# Fetch predefined query results
def fetch_data(query):
    conn = get_connection()
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# AI-powered Scenario Analysis
client = groq.Client(api_key="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")

class ScenarioAnalysisTool(Tool):
    name = "scenario_analysis"
    description = "Analyzes a generated scenario and provides structured insights."
    inputs = {
        "scenario": {"type": "string", "description": "Scenario title."},
        "data_string": {"type": "string", "description": "String representation of the dataset."}
    }
    output_type = "string"

    def forward(self, scenario: str, data_string: str):
        prompt = (f"Analyze the following dataset based on actual trends:\n\n"
                  f"{data_string}\n\n"
                  f"Scenario: {scenario}\n\n"
                  "**Overall Trends**\n"
                  "- Identify key trends from the data.\n"
                  "- Provide only insights based on available data.\n"
                  "- Avoid introducing external information.\n\n"
                  "**Key Insights**\n"
                  "- Summarize major findings based only on this dataset.")

        response = client.chat.completions.create(
            model="qwen-2.5-32b",
            messages=[{"role": "user", "content": prompt}]
        )
        
        return response.choices[0].message.content.strip()
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
    
    /* Toggle button styles */
    div[data-testid="stHorizontalBlock"] > div:first-child button {
        background-color: #0b8793;
        color: white !important;
        border: 1px solid #4AC29A;
        border-radius: 5px;
        padding: 8px 15px;
        font-weight: bold;
        box-shadow: 0 2px 5px rgba(0,0,0,0.2);
        transition: all 0.3s ease;
    }

    div[data-testid="stHorizontalBlock"] > div:first-child button:hover {
        background-color: #4AC29A;
        transform: translateY(-1px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    
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
    
    [data-testid="stSidebar"] .stSelectbox > div, [data-testid="stSidebar"] .stMultiSelect > div {
        background-color: rgba(255,255,255,0.1) !important;
        border: 1px solid rgba(255,255,255,0.2) !important;
        border-radius: 5px;
        color: white !important;
        margin-bottom: 15px;
    }
    
    [data-testid="stSidebar"] .stSelectbox > div:hover, [data-testid="stSidebar"] .stMultiSelect > div:hover {
        border: 1px solid rgba(255,255,255,0.4) !important;
    }
    
    [data-testid="stSidebar"] span[data-baseweb="tag"] {
        background-color: #73C8A9 !important;
        border: none !important;
    }
    
    .logo-title-container {
        display: flex;
        flex-direction: row;
        align-items: center;
        justify-content: space-between;
    }
    .logo img {
        width: 60px;
        border-radius: 50%;
    }
    .app-name {
        font-size: 1.5em;
        font-weight: bold;
    }
   
   
    .stButton button {
        width:100%;
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

    .stButton button:hover {
        background-color: #4AC29A;
        color: white !important;
        box-shadow: 0 3px 7px rgba(0,0,0,0.15);
        transform: translateY(-1px);
    }
    
    a{
        text-decoration: none;
        color: #0F403F !important;
    }
    a:hover{
        color: #0F403F !important;
        text-decoration: none;
    }
    
    /* Chart Improvements */
    .marks{
        border-radius: 15px; /* Rounded corners for the SVG canvas */
        border: 1px solid  #0b8793; /* Greenish border */
        box-shadow: 0px 8px 15px rgba(0, 0, 0, 0.2);
        margin-top: 20px; /* Add some spacing from the buttons */
        padding: 20px; /* Add padding inside the canvas */
        width: 99%; /* Full width */
        background-color: #f9fcfc;
    }
    
    /* Make axes and labels more visible but sharper */
    .chart-wrapper {
        margin-bottom: 30px;
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
    
    .marks .mark-rule line {
        stroke: #ddd !important;
        stroke-width: 1px !important;
    }
    
    /* Numbers on axes */
    .marks text.role-axis-label {
        font-size: 16px !important;
        font-weight: bold !important;
        fill: #333 !important;
    }
    
    /* Analysis text formatting */
    .scenario-analysis {
        background-color: #f9fcfc;
        border-left: 4px solid #0b8793;
        padding: 20px;
        margin-top: 20px;
        border-radius: 0 5px 5px 0;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
    }
    
    .scenario-analysis h3 {
        color: #0b8793;
        margin-bottom: 15px;
    }
    
    .scenario-analysis ul {
        padding-left: 20px;
    }
    
    .scenario-analysis li {
        margin-bottom: 8px;
        line-height: 1.5;
    }
    
    /* Scenario header styling */
    h2 {
        color: #0b8793;
        border-bottom: 2px solid #73C8A9;
        padding-bottom: 8px;
        margin-top: 30px;
        margin-bottom: 20px;
    }
    
""", unsafe_allow_html=True)

# Add the toggle button at the top with a narrower column
toggle_col1, toggle_col2 = st.columns([1, 11])
with toggle_col1:
    st.button(st.session_state.button_text, key="toggle_sidebar_button", on_click=toggle_sidebar)

# Streamlit UI
st.sidebar.image("images/iesa_white.svg", width=150)
st.sidebar.markdown("""<h2>IESA Scenario Analysis</h2>""", unsafe_allow_html=True)

# Fetch available scenarios from DB
scenarios_df = fetch_scenarios()
scenario_categories = {category: list(group["scenario"]) for category, group in scenarios_df.groupby("category")}

# Sidebar - Category Selection
selected_category = st.sidebar.selectbox("Select Category", list(scenario_categories.keys()))

# Sidebar - Multi-Select Scenarios within Category
selected_scenarios = st.sidebar.multiselect("Select Scenarios", scenario_categories[selected_category])

# Check if scenarios selection has changed and auto-hide sidebar if so
if selected_scenarios and selected_scenarios != st.session_state.previous_scenarios:
    auto_hide_sidebar()
    st.session_state.previous_scenarios = selected_scenarios.copy()

# Query Dictionary for Analysis
query_dict = {
    "Future Electricity Demand Growth": "SELECT Year, `Consumption (GWh)`, ((`Consumption (GWh)` - LAG(`Consumption (GWh)`, 1) OVER (ORDER BY Year)) / LAG(`Consumption (GWh)`, 1) OVER (ORDER BY Year) * 100) AS Growth_Rate FROM annual_electricity_data;",
    "Renewable Energy Contribution": "SELECT Year, `Renewable Electricity`, `Total`, (`Renewable Electricity` / `Total`) * 100 AS Renewable_Percentage FROM primary_energy_supplies_by_source_toe;",
    "Power Shortage Risk": "SELECT Year, `Generation (GWh)`, `Consumption (GWh)`, (`Generation (GWh)` - `Consumption (GWh)`) AS Surplus_Deficit FROM annual_electricity_data;",
    "Impact of Industrial Expansion on Electricity Demand": "SELECT Year, Industrial, (Industrial - LAG(Industrial, 1) OVER (ORDER BY Year)) / LAG(Industrial, 1) OVER (ORDER BY Year) * 100 AS Industrial_Growth_Rate FROM electricity_consumption_by_sector_gwh;",
    "Future Gas Demand Forecast": "SELECT Year, `Natural Gas Consumption`, ((`Natural Gas Consumption` - LAG(`Natural Gas Consumption`, 1) OVER (ORDER BY Year)) / LAG(`Natural Gas Consumption`, 1) OVER (ORDER BY Year)) * 100 AS Growth_Rate FROM natural_gas_production_and_consumption;",
    "Gas Production vs. Consumption Balance": "SELECT Year, `Natural Gas Production`, `Natural Gas Consumption`, (`Natural Gas Production` - `Natural Gas Consumption`) AS Surplus_Deficit FROM natural_gas_production_and_consumption;",
    "Total Energy Demand vs. Supply Balance": "SELECT YEAR, `Total Primary Energy Supply (MTOE)`, `Total Final Consumption of Energy (MTOE)`, (`Total Primary Energy Supply (MTOE)` - `Total Final Consumption of Energy (MTOE)`) AS Surplus_Deficit FROM energy_supply_and_consumption_analysis;",
    "Supply Chain Disruptions in Gas Imports": "SELECT Year, `Imports` FROM total_imports_lng;",
    "Sector-Wise Energy Consumption Changes": "SELECT Year, Total FROM sector_wise_energy_consumption;"
}

# Loop through selected scenarios
for scenario in selected_scenarios:
    st.markdown(f"## Scenario: {scenario}")

    # Fetch data
    if scenario in query_dict:
        query = query_dict[scenario]
        data = fetch_data(query)
        
        if data is not None and not data.empty:
            # Dynamic Charts (Two-column layout)
            num_cols = 2
            cols = st.columns(num_cols)
            y_columns = list(data.columns[1:])  # Exclude 'Year' column

            for idx, y_col in enumerate(y_columns):
                with cols[idx % num_cols]:  # Distribute across columns
                    # Create a more visible color scheme
                    color_scheme = alt.Scale(range=['#0b67a0', '#d62728', '#2ca02c', '#9467bd', '#8c564b'])
                    
                    chart = alt.Chart(data).mark_line(
                        point=True,
                        strokeWidth=3.5,
                        clip=True
                    ).encode(
                        x=alt.X("Year:O", title="Year", axis=alt.Axis(
                            labelAngle=0,
                            titleFontSize=16,
                            titleFontWeight='bold',
                            labelFontSize=14,
                            labelFontWeight='bold',
                            tickWidth=2,
                            tickColor='#333333',
                            labelColor='#333333',
                            titleColor='#333333',
                            domainColor='#666666',
                            domainWidth=2
                        )),
                        y=alt.Y(y_col, title=y_col, axis=alt.Axis(
                            titleFontSize=16,
                            titleFontWeight='bold',
                            labelFontSize=14,
                            labelFontWeight='bold',
                            grid=True,
                            gridColor='#e0e0e0',
                            tickWidth=2,
                            tickColor='#333333',
                            labelColor='#333333',
                            titleColor='#333333',
                            domainColor='#666666',
                            domainWidth=2,
                            format=',.0f'  # Format numbers without decimals
                        )),
                        color=alt.value('#0066cc'),  # Set a fixed color for better visibility matching prediction engine
                        tooltip=list(data.columns)
                    ).properties(
                        title={
                            "text": f"{scenario}: Year vs {y_col}",
                            "fontSize": 18,
                            "fontWeight": "bold",
                            "color": "#0b8793"
                        },
                        height=320
                    )
                    
                    # Add points with enhanced visibility
                    points = alt.Chart(data).mark_circle(
                        size=80,
                        opacity=1,
                        stroke='#fff',
                        strokeWidth=1.5
                    ).encode(
                        x="Year:O",
                        y=y_col,
                        color=alt.value('#0066cc'),
                        tooltip=list(data.columns)
                    )
                    
                    # Combine layers
                    final_chart = (chart + points).configure_view(
                        strokeWidth=1,
                        stroke='#ddd'
                    ).configure_axis(
                        domainWidth=2,
                        domainColor='#666666',
                        labelFontWeight='bold',
                        labelColor='#333333',
                        titleColor='#333333',
                        tickColor='#666666'
                    ).configure_title(
                        fontSize=18,
                        font='Arial',
                        fontWeight='bold',
                        anchor='start',
                        color='#0b8793'
                    )

                    st.altair_chart(final_chart, use_container_width=True)
                    
                    # Add a class for CSS to target
                    st.markdown('<div class="chart-wrapper"></div>', unsafe_allow_html=True)
        else:
            st.error(f"No data available for scenario: {scenario}")

    # AI Analysis Button for Each Scenario with auto-hide on click
    if st.sidebar.button(f"Analyze {scenario}", on_click=auto_hide_sidebar):
        analysis_tool = ScenarioAnalysisTool()
        data_string = data.to_string(index=False)
        analysis = analysis_tool.forward(scenario, data_string)
        st.subheader(f"Analysis for {scenario}")
        # Wrap the analysis in a styled div
        st.markdown(f'<div class="scenario-analysis">{analysis}</div>', unsafe_allow_html=True)

# Check if we should rerun the app at the end
if st.session_state.should_rerun:
    st.session_state.should_rerun = False
    st.rerun()