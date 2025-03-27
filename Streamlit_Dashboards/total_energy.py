import mysql.connector
import pandas as pd
import streamlit as st
import altair as alt
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
def total_energy():
    table_name = "energy_supply_and_consumption_analysis"
    gas_data = fetch_table_data(table_name)

    if not gas_data.empty:
        gas_columns = gas_data.columns.tolist()

        st.subheader("📊 Total energy Dashboard")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            if len(gas_columns) > 1:
                chart1 = alt.Chart(gas_data).mark_bar().encode(
                    x=alt.X(gas_columns[0], title=gas_columns[0]),
                    y=alt.Y(gas_columns[1], title=gas_columns[1]),
                    color=alt.Color(gas_columns[0], scale=alt.Scale(scheme="blues"), legend=None)
                ).properties(title="Total Primary Energy Supply (MTOE)")
                st.altair_chart(chart1, use_container_width=True)
            else:
                st.warning("Missing Total Primary Energy Supply (MTOE)")

        with col2:
            if len(gas_columns) > 2:
                chart2 = alt.Chart(gas_data).mark_bar().encode(
                    x=alt.X(gas_columns[0], title=gas_columns[0]),
                    y=alt.Y(gas_columns[2], title=gas_columns[2]),
                    color=alt.Color(gas_columns[0], scale=alt.Scale(scheme="greens"), legend=None)
                ).properties(title="Total Consumption of Energy (MTOE)")
                # st.altair_chart(chart2, use_container_width=True)
                st.altair_chart(chart2.configure_title(fontSize=14, offset=10), use_container_width=True)
            else:
                st.warning("Missing Total Consumption of Energy (MTOE) Data")
            

        with col3:
            if len(gas_columns) > 3:
                chart3 = alt.Chart(gas_data).mark_bar().encode(
                    x=alt.X(gas_columns[0], title=gas_columns[0]),
                    y=alt.Y(gas_columns[3], title=gas_columns[3]),
                    color=alt.Color(gas_columns[0], scale=alt.Scale(scheme="reds"), legend=None)
                ).properties(title="Supply & Consumption Gap (MTOE)")
                st.altair_chart(chart3, use_container_width=True)
            else:
                st.warning("Missing Supply & Consumption Gap (MTOE) Data")

        with col4:
            if len(gas_columns) > 4:
                chart4 = alt.Chart(gas_data).mark_bar().encode(
                    x=alt.X(gas_columns[0], title=gas_columns[0]),
                    y=alt.Y(gas_columns[4], title=gas_columns[4]),
                    color=alt.Color(gas_columns[0], scale=alt.Scale(scheme="oranges"), legend=None)
                ).properties(title="Transformation losses (TTOE)")
                st.altair_chart(chart4, use_container_width=True)
            else:
                st.warning("Missing Transformation losses (TTOE) Data")
        st.write("Natural Gas Production VS Consumption")        
        st.line_chart(gas_data, x=gas_columns[0], y=[gas_columns[1], gas_columns[2]])

        
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            if len(gas_columns) > 1:
                chart5 = alt.Chart(gas_data).mark_bar().encode(
                    x=alt.X(gas_columns[0], title=gas_columns[0]),
                    y=alt.Y(gas_columns[6], title=gas_columns[6]),
                    color=alt.Color(gas_columns[0], scale=alt.Scale(scheme="blues"), legend=None)
                ).properties(title="T&D losses (TTOE)")
                st.altair_chart(chart5, use_container_width=True)
            else:
                st.warning("Missing T&D losses (TTOE)")

        with col2:
            if len(gas_columns) > 2:
                chart6 = alt.Chart(gas_data).mark_bar().encode(
                    x=alt.X(gas_columns[0], title=gas_columns[0]),
                    y=alt.Y(gas_columns[8], title=gas_columns[8]),
                    color=alt.Color(gas_columns[0], scale=alt.Scale(scheme="greens"), legend=None)
                ).properties(title="Total Losses")
                # st.altair_chart(chart2, use_container_width=True)
                st.altair_chart(chart6.configure_title(fontSize=14, offset=10), use_container_width=True)
            else:
                st.warning("Missing Total Losses Data")
            

        with col3:
            if len(gas_columns) > 3:
                chart7 = alt.Chart(gas_data).mark_bar().encode(
                    x=alt.X(gas_columns[0], title=gas_columns[0]),
                    y=alt.Y(gas_columns[9], title=gas_columns[9]),
                    color=alt.Color(gas_columns[0], scale=alt.Scale(scheme="reds"), legend=None)
                ).properties(title="Energy used  in Transformation")
                st.altair_chart(chart7, use_container_width=True)
            else:
                st.warning("Missing Energy used  in Transformation Data")

        with col4:
            if len(gas_columns) > 4:
                chart8 = alt.Chart(gas_data).mark_bar().encode(
                    x=alt.X(gas_columns[0], title=gas_columns[0]),
                    y=alt.Y(gas_columns[10], title=gas_columns[10]),
                    color=alt.Color(gas_columns[0], scale=alt.Scale(scheme="oranges"), legend=None)
                ).properties(title="Energy sector own use")
                st.altair_chart(chart8, use_container_width=True)
            else:
                st.warning("Missing Energy sector own use Data")

        # st.write("Natural Gas Production VS Consumption")        
        # st.line_chart(gas_data, x=gas_columns[0], y=[gas_columns[1], gas_columns[2]])

    else:
        st.warning("No data available for natural gas production and consumption.")
        