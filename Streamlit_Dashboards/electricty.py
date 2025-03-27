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
def electricty_dashboard():
     # Fetch Annual Electricity Data (First Row Only)
    table_name = "annual_electricity_data"
    electricity_data = fetch_table_data(table_name)

    # Fetch Sector-wise Electricity Consumption Data
    sector_table_name = "electricity_consumption_by_sector_gwh"
    sector_data = fetch_table_data(sector_table_name)

    province_table_name = "province_wise_electricity_consumption_gwh"
    province_data = fetch_table_data(province_table_name)

    if not electricity_data.empty and not sector_data.empty:
        electricity_columns = electricity_data.columns.tolist()
        sector_columns = sector_data.columns.tolist()
        province_columns = province_data.columns.tolist()

        st.subheader("📊 Electricity Data Visualization")

        # First Row Data Visualization
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            if len(electricity_columns) > 1:
                chart1 = alt.Chart(electricity_data).mark_bar().encode(
                    x=alt.X(electricity_columns[0], title=electricity_columns[0]),
                    y=alt.Y(electricity_columns[1], title=electricity_columns[1]),
                    color=alt.Color(electricity_columns[0], scale=alt.Scale(scheme="blues"), legend=None)
                ).properties(title="Installed Capacity (GWh)")
                st.altair_chart(chart1, use_container_width=True)
            else:
                st.warning("Missing Installed Capacity Data")

        with col2:
            if len(electricity_columns) > 2:
                chart2 = alt.Chart(electricity_data).mark_bar().encode(
                    x=alt.X(electricity_columns[0], title=electricity_columns[0]),
                    y=alt.Y(electricity_columns[2], title=electricity_columns[2]),
                    color=alt.Color(electricity_columns[0], scale=alt.Scale(scheme="greens"), legend=None)
                ).properties(title="Electricity Generation")
                st.altair_chart(chart2, use_container_width=True)
            else:
                st.warning("Missing Electricity Generation Data")

        with col3:
            if len(electricity_columns) > 3:
                chart3 = alt.Chart(electricity_data).mark_bar().encode(
                    x=alt.X(electricity_columns[0], title=electricity_columns[0]),
                    y=alt.Y(electricity_columns[3], title=electricity_columns[3]),
                    color=alt.Color(electricity_columns[0], scale=alt.Scale(scheme="reds"), legend=None)
                ).properties(title="Electricity Import")
                st.altair_chart(chart3, use_container_width=True)
            else:
                st.warning("Missing Electricity Import Data")

        with col4:
            if len(electricity_columns) > 4:
                chart4 = alt.Chart(electricity_data).mark_bar().encode(
                    x=alt.X(electricity_columns[0], title=electricity_columns[0]),
                    y=alt.Y(electricity_columns[4], title=electricity_columns[4]),
                    color=alt.Color(electricity_columns[0], scale=alt.Scale(scheme="oranges"), legend=None)
                ).properties(title="Electricity Consumption")
                st.altair_chart(chart4, use_container_width=True)
            else:
                st.warning("Missing Electricity Consumption Data")
        st.line_chart(electricity_data, x=electricity_columns[0], y=[electricity_columns[1], electricity_columns[2],electricity_columns[3],electricity_columns[4]])
        st.subheader("📊 Sector-wise Electricity Consumption")

        # Sector-wise Consumption Visualization
        sec_col1, sec_col2, sec_col3, sec_col4 = st.columns(4)

        with sec_col1:
            if len(sector_columns) > 1:
                sec_chart1 = alt.Chart(sector_data).mark_bar().encode(
                    x=alt.X(sector_columns[0], title=sector_columns[0]),
                    y=alt.Y(sector_columns[1], title=sector_columns[1]),
                    color=alt.Color(sector_columns[0], scale=alt.Scale(scheme="purpleblue"), legend=None)
                ).properties(title="Residential Consumption")
                st.altair_chart(sec_chart1, use_container_width=True)
            else:
                st.warning("Missing Residential Data")

        with sec_col2:
            if len(sector_columns) > 2:
                sec_chart2 = alt.Chart(sector_data).mark_bar().encode(
                    x=alt.X(sector_columns[0], title=sector_columns[0]),
                    y=alt.Y(sector_columns[2], title=sector_columns[2]),
                    color=alt.Color(sector_columns[0], scale=alt.Scale(scheme="blueorange"), legend=None)
                ).properties(title="Commercial Consumption")
                st.altair_chart(sec_chart2, use_container_width=True)
            else:
                st.warning("Missing Commercial Data")

        with sec_col3:
            if len(sector_columns) > 3:
                sec_chart3 = alt.Chart(sector_data).mark_bar().encode(
                    x=alt.X(sector_columns[0], title=sector_columns[0]),
                    y=alt.Y(sector_columns[3], title=sector_columns[3]),
                    color=alt.Color(sector_columns[0], scale=alt.Scale(scheme="yellowgreen"), legend=None)
                ).properties(title="Industrial Consumption")
                st.altair_chart(sec_chart3, use_container_width=True)
            else:
                st.warning("Missing Industrial Data")

        with sec_col4:
            if len(sector_columns) > 4:
                sec_chart4 = alt.Chart(sector_data).mark_bar().encode(
                    x=alt.X(sector_columns[0], title=sector_columns[0]),
                    y=alt.Y(sector_columns[4], title=sector_columns[4]),
                    color=alt.Color(sector_columns[0], scale=alt.Scale(scheme="redblue"), legend=None)
                ).properties(title="Agricultural Consumption")
                st.altair_chart(sec_chart4, use_container_width=True)
            else:
                st.warning("Missing Agricultural Data")

        thrd_col1, thrd_col2,thrd_col3, thrd_col4 = st.columns(4)
        with thrd_col1:
            if len(sector_columns) > 1:
                sec_chart1 = alt.Chart(sector_data).mark_bar().encode(
                    x=alt.X(sector_columns[0], title=sector_columns[0]),
                    y=alt.Y(sector_columns[5], title=sector_columns[5]),
                    color=alt.Color(sector_columns[0], scale=alt.Scale(scheme="purpleblue"), legend=None)
                ).properties(title="Street Light Consumption")
                st.altair_chart(sec_chart1, use_container_width=True)
            else:
                st.warning("Missing Residential Data")

        with thrd_col2:
            if len(sector_columns) > 2:
                sec_chart2 = alt.Chart(sector_data).mark_bar().encode(
                    x=alt.X(sector_columns[0], title=sector_columns[0]),
                    y=alt.Y(sector_columns[7], title=sector_columns[7]),
                    color=alt.Color(sector_columns[0], scale=alt.Scale(scheme="blueorange"), legend=None)
                ).properties(title="Bulk Supply Consumption")
                st.altair_chart(sec_chart2, use_container_width=True)
            else:
                st.warning("Traction Data")

        with thrd_col3:
            if len(sector_columns) > 3:
                sec_chart3 = alt.Chart(sector_data).mark_bar().encode(
                    x=alt.X(sector_columns[0], title=sector_columns[0]),
                    y=alt.Y(sector_columns[8], title=sector_columns[8]),
                    color=alt.Color(sector_columns[0], scale=alt.Scale(scheme="yellowgreen"), legend=None)
                ).properties(title="Other Govt Consumption")
                st.altair_chart(sec_chart3, use_container_width=True)
            else:
                st.warning("Bulk Supply Data")

        with thrd_col4:
            if len(sector_columns) > 4:
                sec_chart4 = alt.Chart(sector_data).mark_bar().encode(
                    x=alt.X(sector_columns[0], title=sector_columns[0]),
                    y=alt.Y(sector_columns[9], title=sector_columns[9]),
                    color=alt.Color(sector_columns[0], scale=alt.Scale(scheme="redblue"), legend=None)
                ).properties(title="Total Consumption")
                st.altair_chart(sec_chart4, use_container_width=True)
            else:
                st.warning("Other Govt Data")  
        st.line_chart(sector_data, x=sector_columns[0], y=[sector_columns[1], sector_columns[2],sector_columns[3],sector_columns[4],sector_columns[5], sector_columns[7],sector_columns[8],sector_columns[9]])      
       
        st.subheader("📊 Province-wise Electricity Consumption")
        frth_col1, frth_col2,frth_col3 = st.columns(3)
        with frth_col1:
            if len(province_columns) > 1:
                frth_chart1 = alt.Chart(province_data).mark_bar().encode(
                    x=alt.X(province_columns[0], title=province_columns[0]),
                    y=alt.Y(province_columns[1], title=province_columns[1]),
                    color=alt.Color(province_columns[0], scale=alt.Scale(scheme="purpleblue"), legend=None)
                ).properties(title="Punjab Consumption")
                st.altair_chart(frth_chart1, use_container_width=True)
            else:
                st.warning("Missing Residential Data")

        with frth_col2:
            if len(province_columns) > 2:
                frth_chart2 = alt.Chart(province_data).mark_bar().encode(
                    x=alt.X(province_columns[0], title=province_columns[0]),
                    y=alt.Y(province_columns[2], title=province_columns[2]),
                    color=alt.Color(province_columns[0], scale=alt.Scale(scheme="blueorange"), legend=None)
                ).properties(title="Sindh Consumption")
                st.altair_chart(frth_chart2, use_container_width=True)
            else:
                st.warning("Traction Data")

        with frth_col3:
            if len(province_columns) > 3:
                frth_chart3 = alt.Chart(province_data).mark_bar().encode(
                    x=alt.X(province_columns[0], title=province_columns[0]),
                    y=alt.Y(province_columns[3], title=province_columns[3]),
                    color=alt.Color(province_columns[0], scale=alt.Scale(scheme="yellowgreen"), legend=None)
                ).properties(title="KPK Consumption")
                st.altair_chart(frth_chart3, use_container_width=True)
            else:
                st.warning("Bulk Supply Data")

        with frth_col1:
            if len(province_columns) > 4:
                frth_chart4 = alt.Chart(province_data).mark_bar().encode(
                    x=alt.X(province_columns[0], title=province_columns[0]),
                    y=alt.Y(province_columns[4], title=province_columns[4]),
                    color=alt.Color(province_columns[0], scale=alt.Scale(scheme="redblue"), legend=None)
                ).properties(title="Balochistan Consumption")
                st.altair_chart(frth_chart4, use_container_width=True)
            else:
                st.warning("Other Govt Data")  
        with frth_col2:
            if len(province_columns) > 4:
                frth_chart4 = alt.Chart(province_data).mark_bar().encode(
                    x=alt.X(province_columns[0], title=province_columns[0]),
                    y=alt.Y(province_columns[5], title=province_columns[5]),
                    color=alt.Color(province_columns[0], scale=alt.Scale(scheme="redblue"), legend=None)
                ).properties(title="AJK Consumption")
                st.altair_chart(frth_chart4, use_container_width=True)
            else:
                st.warning("Other Govt Data")   
        with frth_col3:
            if len(province_columns) > 4:
                frth_chart4 = alt.Chart(province_data).mark_bar().encode(
                    x=alt.X(province_columns[0], title=province_columns[0]),
                    y=alt.Y(province_columns[6], title=province_columns[6]),
                    color=alt.Color(province_columns[0], scale=alt.Scale(scheme="redblue"), legend=None)
                ).properties(title="T&D  Losses")
                st.altair_chart(frth_chart4, use_container_width=True)
            else:
                st.warning("Other Govt Data")                  
        st.line_chart(province_data, x=province_columns[0], y=[province_columns[1], province_columns[2],province_columns[3],province_columns[4],province_columns[5],province_columns[6]])      
    else:
          st.warning("No data available for the selected tables.")