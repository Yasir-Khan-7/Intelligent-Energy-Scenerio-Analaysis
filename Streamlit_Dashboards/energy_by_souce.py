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
def energy_by_souce_dashboard():

     # Fetch Supplies Data (First Row Only)
    supplies_table_name = "primary_energy_supplies_by_source_toe"
    supplies_data = fetch_table_data(supplies_table_name)

    # Fetch  Consumption Data
    consumption_table_name = "final_energy_consumption_by_source_toe"
    consumption_data = fetch_table_data(consumption_table_name)

    if not supplies_data.empty and not consumption_data.empty:
        supplies_data_columns = supplies_data.columns.tolist()
        consumption_columns = consumption_data.columns.tolist()

        st.subheader("📊 Energy Supplies By Source")
        # First Row Data Visualization
        col1, col2, col3, col4, col5 = st.columns(5)

        with col1:
            if len(supplies_data_columns) > 1:
                chart1 = alt.Chart(supplies_data).mark_bar().encode(
                    x=alt.X(supplies_data_columns[0], title=supplies_data_columns[0]),
                    y=alt.Y(supplies_data_columns[1], title=supplies_data_columns[1]),
                    color=alt.Color(supplies_data_columns[0], scale=alt.Scale(scheme="blues"), legend=None)
                ).properties(title="Oil")
                st.altair_chart(chart1, use_container_width=True)
            else:
                st.warning("Missing Oil Data")

        with col2:
            if len(supplies_data_columns) > 2:
                chart2 = alt.Chart(supplies_data).mark_bar().encode(
                    x=alt.X(supplies_data_columns[0], title=supplies_data_columns[0]),
                    y=alt.Y(supplies_data_columns[2], title=supplies_data_columns[2]),
                    color=alt.Color(supplies_data_columns[0], scale=alt.Scale(scheme="greens"), legend=None)
                ).properties(title="Gas")
                st.altair_chart(chart2, use_container_width=True)
            else:
                st.warning("Missing Gas Data")

        with col3:
            if len(supplies_data_columns) > 3:
                chart3 = alt.Chart(supplies_data).mark_bar().encode(
                    x=alt.X(supplies_data_columns[0], title=supplies_data_columns[0]),
                    y=alt.Y(supplies_data_columns[3], title=supplies_data_columns[3]),
                    color=alt.Color(supplies_data_columns[0], scale=alt.Scale(scheme="reds"), legend=None)
                ).properties(title="LNG  Import")
                st.altair_chart(chart3, use_container_width=True)
            else:
                st.warning("Missing Electricity Import Data")

        with col4:
            if len(supplies_data_columns) > 4:
                chart4 = alt.Chart(supplies_data).mark_bar().encode(
                    x=alt.X(supplies_data_columns[0], title=supplies_data_columns[0]),
                    y=alt.Y(supplies_data_columns[4], title=supplies_data_columns[4]),
                    color=alt.Color(supplies_data_columns[0], scale=alt.Scale(scheme="oranges"), legend=None)
                ).properties(title="LNG local Supply")
                st.altair_chart(chart4, use_container_width=True)
            else:
                st.warning("Missing Electricity Consumption Data")

        with col5:
            if len(supplies_data_columns) > 4:
                chart4 = alt.Chart(supplies_data).mark_bar().encode(
                    x=alt.X(supplies_data_columns[0], title=supplies_data_columns[0]),
                    y=alt.Y(supplies_data_columns[5], title=supplies_data_columns[5]),
                    color=alt.Color(supplies_data_columns[0], scale=alt.Scale(scheme="purpleblue"), legend=None)
                ).properties(title="Coal")
                st.altair_chart(chart4, use_container_width=True)
            else:
                st.warning("Missing Coal Data")
        sec_col1, sec_col2,sec_col3,sec_col4 = st.columns(4)
        with sec_col1:
            if len(supplies_data_columns) > 1:
                chart1 = alt.Chart(supplies_data).mark_bar().encode(
                    x=alt.X(supplies_data_columns[0], title=supplies_data_columns[0]),
                    y=alt.Y(supplies_data_columns[6], title=supplies_data_columns[6]),
                    color=alt.Color(supplies_data_columns[0], scale=alt.Scale(scheme="blues"), legend=None)
                ).properties(title="Hydro Electricity")
                st.altair_chart(chart1, use_container_width=True)
            else:
                st.warning("Missing Hydro Electricity Data")

        with sec_col2:
            if len(supplies_data_columns) > 2:
                chart2 = alt.Chart(supplies_data).mark_bar().encode(
                    x=alt.X(supplies_data_columns[0], title=supplies_data_columns[0]),
                    y=alt.Y(supplies_data_columns[7], title=supplies_data_columns[8]),
                    color=alt.Color(supplies_data_columns[0], scale=alt.Scale(scheme="greens"), legend=None)
                ).properties(title="Nuclear electricity")
                st.altair_chart(chart2, use_container_width=True)
            else:
                st.warning("Missing Nuclear electricity Data")

        with sec_col3:
            if len(supplies_data_columns) > 3:
                chart3 = alt.Chart(supplies_data).mark_bar().encode(
                    x=alt.X(supplies_data_columns[0], title=supplies_data_columns[0]),
                    y=alt.Y(supplies_data_columns[8], title=supplies_data_columns[8]),
                    color=alt.Color(supplies_data_columns[0], scale=alt.Scale(scheme="reds"), legend=None)
                ).properties(title="Imported electricity")
                st.altair_chart(chart3, use_container_width=True)
            else:
                st.warning("Missing Imported electricity Data")

        with sec_col4:
            if len(supplies_data_columns) > 4:
                chart4 = alt.Chart(supplies_data).mark_bar().encode(
                    x=alt.X(supplies_data_columns[0], title=supplies_data_columns[0]),
                    y=alt.Y(supplies_data_columns[9], title=supplies_data_columns[9]),
                    color=alt.Color(supplies_data_columns[0], scale=alt.Scale(scheme="oranges"), legend=None)
                ).properties(title="Renewable Electricity")
                st.altair_chart(chart4, use_container_width=True)
            else:
                st.warning("Missing Renewable Electricity Data")        
        st.line_chart(supplies_data, x=supplies_data_columns[0], y=[supplies_data_columns[1], supplies_data_columns[2],supplies_data_columns[3],supplies_data_columns[4],supplies_data_columns[5], supplies_data_columns[6],supplies_data_columns[7],supplies_data_columns[8],supplies_data_columns[9]])

        #  Consumption Visualization
        # final_energy_consumption_by_source_toe
        st.subheader("📊 Energy Consumption By Source")
        sec_col1, sec_col2,sec_col3 = st.columns(3)
        with sec_col1:
            if len(consumption_columns) > 1:
                frth_chart1 = alt.Chart(consumption_data).mark_bar().encode(
                    x=alt.X(consumption_columns[0], title=consumption_columns[0]),
                    y=alt.Y(consumption_columns[1], title=consumption_columns[1]),
                    color=alt.Color(consumption_columns[0], scale=alt.Scale(scheme="purpleblue"), legend=None)
                ).properties(title="Oil Consumption")
                st.altair_chart(frth_chart1, use_container_width=True)
            else:
                st.warning("Missing Oil Data")

        with sec_col2:
            if len(consumption_columns) > 2:
                frth_chart2 = alt.Chart(consumption_data).mark_bar().encode(
                    x=alt.X(consumption_columns[0], title=consumption_columns[0]),
                    y=alt.Y(consumption_columns[2], title=consumption_columns[2]),
                    color=alt.Color(consumption_columns[0], scale=alt.Scale(scheme="blueorange"), legend=None)
                ).properties(title="Gas Consumption")
                st.altair_chart(frth_chart2, use_container_width=True)
            else:
                st.warning("Gas Data")

        with sec_col3:
            if len(consumption_columns) > 3:
                frth_chart3 = alt.Chart(consumption_data).mark_bar().encode(
                    x=alt.X(consumption_columns[0], title=consumption_columns[0]),
                    y=alt.Y(consumption_columns[3], title=consumption_columns[3]),
                    color=alt.Color(consumption_columns[0], scale=alt.Scale(scheme="yellowgreen"), legend=None)
                ).properties(title="LPG Consumption")
                st.altair_chart(frth_chart3, use_container_width=True)
            else:
                st.warning("LPG Data")

        with sec_col1:
            if len(consumption_columns) > 4:
                frth_chart4 = alt.Chart(consumption_data).mark_bar().encode(
                    x=alt.X(consumption_columns[0], title=consumption_columns[0]),
                    y=alt.Y(consumption_columns[4], title=consumption_columns[4]),
                    color=alt.Color(consumption_columns[0], scale=alt.Scale(scheme="redblue"), legend=None)
                ).properties(title="Coal Consumption")
                st.altair_chart(frth_chart4, use_container_width=True)
            else:
                st.warning("Coal Data")  
        with sec_col2:
            if len(consumption_columns) > 4:
                frth_chart4 = alt.Chart(consumption_data).mark_bar().encode(
                    x=alt.X(consumption_columns[0], title=consumption_columns[0]),
                    y=alt.Y(consumption_columns[5], title=consumption_columns[5]),
                    color=alt.Color(consumption_columns[0], scale=alt.Scale(scheme="redblue"), legend=None)
                ).properties(title="Electricity Consumption")
                st.altair_chart(frth_chart4, use_container_width=True)
            else:
                st.warning("Electricity Data")   
        with sec_col3:
            if len(consumption_columns) > 4:
                frth_chart4 = alt.Chart(consumption_data).mark_bar().encode(
                    x=alt.X(consumption_columns[0], title=consumption_columns[0]),
                    y=alt.Y(consumption_columns[6], title=consumption_columns[6]),
                    color=alt.Color(consumption_columns[0], scale=alt.Scale(scheme="redblue"), legend=None)
                ).properties(title="Total consumption")
                st.altair_chart(frth_chart4, use_container_width=True)
            else:
                st.warning("Total Consumption")                  
        st.line_chart(consumption_data, x=consumption_columns[0], y=[consumption_columns[1], consumption_columns[2],consumption_columns[3],consumption_columns[4],consumption_columns[5],consumption_columns[6]])      
    else:
          st.warning("No data available for the selected tables.")