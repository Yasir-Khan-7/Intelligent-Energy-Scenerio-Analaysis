import mysql.connector
import pandas as pd
import streamlit as st
import altair as alt
from electricty import electricty_dashboard
from total_energy import total_energy
from gas import gas_dashboard
from energy_by_souce import energy_by_souce_dashboard


st.set_page_config(page_title="IESA Dashboard", layout="wide", page_icon="📊")
col1,col2,col3,col4,col5,col6,col7,col8,col9,col10,col11,col12=st.columns(12)
with col1:
    st.button("Dashbaord")
with col2:
    st.button("Scenerio")
with col3:
    st.button("Predictors")
with col4:
    st.button("Reports")            
image_path = "images/iesa_white.svg"
# Establish Database Connection
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        port="3306",
        user="root",
        passwd="admin123",
        db="iesa_db"
    )

# Fetch Data from a Table
def fetch_table_data(table_name):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        query = f"SELECT * FROM `{table_name}`"
        cursor.execute(query)
        rows = cursor.fetchall()
        if not rows:
            return pd.DataFrame()
        columns = [desc[0] for desc in cursor.description]
        data = pd.DataFrame(rows, columns=columns)

        # Convert MW to GWh if applicable
        if "Installed Capacity (MW)" in data.columns:
            data["Installed Capacity (MW)"] = (data["Installed Capacity (MW)"] * 8760) / 1000
            data = data.rename(columns={"Installed Capacity (MW)": "Installed Capacity (GWh)"})

        # Convert all numeric columns to float for visualization
        for col in data.columns[1:]:
            data[col] = pd.to_numeric(data[col], errors="coerce")
        data.fillna(0, inplace=True)

    except Exception as e:
        print(f"Error fetching data from {table_name}: {e}")
        data = pd.DataFrame()
    finally:
        conn.close()
    
    return data

# Sidebar Styling
st.markdown("""
    <style>
    header {
        border-bottom: 3px solid  #136a8a !important; 
    }
    [data-testid="stSidebar"] {
        background: linear-gradient(135deg, #73C8A9, #0b8793);
        color: white;
        margin-top: 58px;
    }
    </style>
""", unsafe_allow_html=True)

st.sidebar.image(image_path, width=150)
st.sidebar.markdown("<h2>Data Planner Dashboard</h2>", unsafe_allow_html=True)

selected_table = st.sidebar.selectbox("Choose Data Type", ["Electricity", "GAS","Total Energy","Energy By Souce"])

if selected_table == "Electricity":
    electricty_dashboard()
elif selected_table == "GAS":
    gas_dashboard()
elif selected_table == "Energy By Souce":
    energy_by_souce_dashboard()   
else:
    total_energy()