import mysql.connector
import pandas as pd
import streamlit as st
import altair as alt

# Function to get a database connection
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        port="3306",
        user="root",
        passwd="admin123",
        db="iesa_db"
    )
def circular_progress(label, value, max_value, color):
    percentage = (value / max_value) * 100
    st.markdown(
        f"""
        <div style='text-align: center;'>
            <h4>{label}</h4>
            <div style='position: relative; width: 150px; height: 150px; margin: auto;'>
                <svg width='150' height='150'>
                    <circle cx='75' cy='75' r='65' stroke='#4A5568' stroke-width='10' fill='none'/>
                    <circle cx='75' cy='75' r='65' stroke='{color}' stroke-width='10' fill='none'
                        stroke-dasharray='{percentage * 4.08}, 408' transform='rotate(-90 75 75)'/>
                </svg>
                <div style='position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); font-size: 24px;'>
                    {int(percentage)}%
                </div>
            </div>
            <p>{value:,.2f} / {max_value:,.2f}</p>
        </div>
        """,
        unsafe_allow_html=True
    )
# Fetch data from a table
def fetch_table_data(table_name):
    try:
        conn = get_connection()
        with conn.cursor() as cursor:
            query = f"SELECT * FROM `{table_name}`"
            cursor.execute(query)
            rows = cursor.fetchall()
            if not rows:
                return pd.DataFrame()
            columns = [desc[0] for desc in cursor.description]
            data = pd.DataFrame(rows, columns=columns)

            # Convert numeric columns to float
            for col in data.columns[1:]:
                data[col] = pd.to_numeric(data[col], errors="coerce")
            data.fillna(0, inplace=True)
    except Exception as e:
        st.error(f"Error fetching data: {e}")
        data = pd.DataFrame()
    finally:
        conn.close()

    return data

# Gas Dashboard for Business Intelligence
def gas_dashboard():
    st.title("📊 Natural Gas BI Dashboard")
    
    table_name = "natural_gas_production_and_consumption"
    gas_data = fetch_table_data(table_name)

    if not gas_data.empty:
        gas_columns = gas_data.columns.tolist()
        
        # Sidebar Filters
        st.sidebar.header("🔍 Filters")
        years = gas_data[gas_columns[0]].unique().tolist()
        years.insert(0, "All")  # Add "All" option at the start
        selected_year = st.sidebar.selectbox("Select Year", years, index=0)

        # Filter data
        if selected_year != "All":
            filtered_data = gas_data[gas_data[gas_columns[0]] == selected_year]
        else:
            filtered_data = gas_data

        # KPIs
        st.subheader(f"📈 Key Metrics ({'All Years' if selected_year == 'All' else selected_year})")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(label="Total Gas Production", value=f"{filtered_data[gas_columns[1]].sum():,.2f} Bcf")
        with col2:
            st.metric(label="Total Gas Consumption", value=f"{filtered_data[gas_columns[2]].sum():,.2f} Bcf")
        with col3:
            if filtered_data[gas_columns[1]].sum() > 0:
                ratio = (filtered_data[gas_columns[2]].sum() / filtered_data[gas_columns[1]].sum()) * 100
                st.metric(label="Consumption vs. Production Ratio", value=f"{ratio:.2f}%")
            else:
                st.metric(label="Consumption vs. Production Ratio", value="N/A")

        # Charts Layout
        
        st.subheader("📊 Gas Production & Consumption Trends")
        col1,col2=st.columns(2)
        with col1:
            chart1 = alt.Chart(filtered_data).mark_bar().encode(
                x=alt.X(gas_columns[0], title="Year"),
                y=alt.Y(gas_columns[1], title="Gas Production"),
                color=alt.Color(gas_columns[0], scale=alt.Scale(scheme="blues"), legend=None)
            ).properties(title="Gas Production Over Time")
            st.altair_chart(chart1, use_container_width=True)
        with col2:
            chart2 = alt.Chart(filtered_data).mark_bar().encode(
            x=alt.X(gas_columns[0], title="Year"),
            y=alt.Y(gas_columns[2], title="Gas Consumption"),
            color=alt.Color(gas_columns[0], scale=alt.Scale(scheme="greens"), legend=None)
        ).properties(title="Gas Consumption Over Time")
            st.altair_chart(chart2, use_container_width=True)

        col1,col2=st.columns(2)
        with col1:    
        # Line Chart for Trend Analysis
            st.subheader("📈 Production vs. Consumption Trend")
            st.line_chart(filtered_data.set_index(gas_columns[0])[[gas_columns[1], gas_columns[2]]])
        with col2:
            total_production = filtered_data[gas_columns[1]].sum()
            total_consumption = filtered_data[gas_columns[2]].sum()    
            cons_ratio = (total_consumption / total_production) * 100 if total_production > 0 else 0
            circular_progress("Consumption vs Production", cons_ratio, 100, "#F58518")        

        # Additional Financial Insights
        st.subheader("💰 Financial Overview")
        col4, col5 = st.columns(2)
        with col4:
            chart3 = alt.Chart(filtered_data).mark_bar().encode(
                x=alt.X(gas_columns[0], title="Year"),
                y=alt.Y(gas_columns[3], title="Gas Revenue (PKR Billions)"),
                color=alt.Color(gas_columns[3],type='quantitative', scale=alt.Scale(scheme="greens"), legend=None)
            ).properties(title="Gas Revenue Trend")
            st.altair_chart(chart3, use_container_width=True)

        with col5:
            chart4 = alt.Chart(filtered_data).mark_bar().encode(
                x=alt.X(gas_columns[0], title="Year"),
                y=alt.Y(gas_columns[4], title="Gas Import Costs (PKR Billions)"),
                color=alt.Color(gas_columns[0], scale=alt.Scale(scheme="oranges"), legend=None)
            ).properties(title="Gas Import Costs")
            st.altair_chart(chart4, use_container_width=True)

    else:
        st.warning("⚠ No data available for natural gas production and consumption.")
