import mysql.connector
import pandas as pd
import streamlit as st
import altair as alt
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures, LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.ensemble import RandomForestRegressor
from sklearn.svm import SVR

st.set_page_config(page_title="IESA Dashboard", layout="wide", page_icon="📊")
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
        box-shadow: 5px 0 10px rgba(0, 0, 0, 0.2);
        border-right: 2px solid #4AC29A;
    }
    .sidebar-content {
        margin-top: -60px;
        padding: 20px;
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
    
    [data-testid="stBaseButton-secondary"]{
        background-color: #0b8793 !important;
        width:100% !important;
        border: 1px solid #4AC29A;
        border-radius: 5px;
        margin-bottom: 10px;
        color: white !important;
        font-weight: 600;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }

    [data-testid="stBaseButton-secondary"]:hover {
        background-color: #0b8793;
        color: white !important;
        transform: translateY(-2px);
        box-shadow: 0 6px 8px rgba(0, 0, 0, 0.15);
        transition: all 0.2s ease;
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
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }

    .stButton button:hover {
        background-color: #0b8793;
        color: white !important;
        transform: translateY(-2px);
        box-shadow: 0 6px 8px rgba(0, 0, 0, 0.15);
    }
    
 
     [data-testid="stWidgetLabel"]{
            color:white !important;
            margin-bottom: 10px;
            }
    /* Sidebar header styling */
    [data-testid="stSidebar"] h2 {
        color: white;
        font-size: 24px;
        padding-bottom: 10px;
        border-bottom: 2px solid rgba(255, 255, 255, 0.2);
        margin-bottom: 20px;
        text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.2);
    }
    
    .marks{
        border-radius: 15px; /* Rounded corners for the SVG canvas */
        border: 1px solid  #0b8793; /* Greenish border */
         box-shadow: 0px 8px 15px rgba(0, 0, 0, 0.2);
        margin-top: 20px; /* Add some spacing from the buttons */
        padding: 10px; /* Add padding inside the canvas */
        width: 99%; /* Full width */
    }
    </style>

 
""", unsafe_allow_html=True)


if "results" not in st.session_state:
    st.session_state.results = []

# Database connection
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        port="3306",
        user="root",
        passwd="admin123",
        db="iesa_db"
    )

# Fetch tables
def fetch_tables():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SHOW TABLES")
        tables = [table[0] for table in cursor.fetchall()]
        conn.close()
        return tables
    except Exception as e:
        st.error(f"Error fetching tables: {e}")
        return []

# Fetch table data
def fetch_table_data(table_name):
    conn = get_connection()
    query = f"SELECT * FROM {table_name}"
    data = pd.read_sql(query, conn)
    conn.close()
    return data

# Ensure X column is numeric
def preprocess_x_column(data, x_column):
    if data[x_column].dtype == 'object':
        try:
            data[x_column] = data[x_column].astype(str).str[:4].astype(int)
        except:
            encoder = LabelEncoder()
            data[x_column] = encoder.fit_transform(data[x_column])
    return data

# Regression Functions
def perform_linear_regression(data, x_column, y_column):
    data = preprocess_x_column(data, x_column)
    X, y = data[[x_column]].values, data[y_column].values
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    model = LinearRegression()
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    future_data = pd.DataFrame({x_column: np.arange(data[x_column].max() + 1, data[x_column].max() + 6)})
    future_data[y_column] = model.predict(future_data[[x_column]])

    return model, mean_squared_error(y_test, y_pred), r2_score(y_test, y_pred), future_data

def perform_polynomial_regression(data, x_column, y_column, degree=2):
    data = preprocess_x_column(data, x_column)
    X, y = data[[x_column]].values, data[y_column].values
    poly = PolynomialFeatures(degree=degree)
    X_poly = poly.fit_transform(X)
    
    X_train, X_test, y_train, y_test = train_test_split(X_poly, y, test_size=0.2, random_state=42)
    model = LinearRegression()
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    future_data = pd.DataFrame({x_column: np.arange(data[x_column].max() + 1, data[x_column].max() + 6)})
    future_data[y_column] = model.predict(poly.transform(future_data[[x_column]]))

    return model, poly, mean_squared_error(y_test, y_pred), r2_score(y_test, y_pred), future_data

def perform_random_forest_regression(data, x_column, y_column):
    data = preprocess_x_column(data, x_column)
    X, y = data[[x_column]].values, data[y_column].values
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    future_data = pd.DataFrame({x_column: np.arange(data[x_column].max() + 1, data[x_column].max() + 6)})
    future_data[y_column] = model.predict(future_data[[x_column]])

    return model, mean_squared_error(y_test, y_pred), r2_score(y_test, y_pred), future_data

def perform_svr(data, x_column, y_column):
    data = preprocess_x_column(data, x_column)
    X, y = data[[x_column]].values, data[y_column].values

    scaler_x, scaler_y = StandardScaler(), StandardScaler()
    X_scaled = scaler_x.fit_transform(X)
    y_scaled = scaler_y.fit_transform(y.reshape(-1, 1)).flatten()

    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y_scaled, test_size=0.2, random_state=42)

    model = SVR(kernel="rbf", C=100, gamma=0.1, epsilon=0.1)
    model.fit(X_train, y_train)
    y_pred_scaled = model.predict(X_test)

    y_pred = scaler_y.inverse_transform(y_pred_scaled.reshape(-1, 1)).flatten()
    y_test_actual = scaler_y.inverse_transform(y_test.reshape(-1, 1)).flatten()

    future_x = np.arange(data[x_column].max() + 1, data[x_column].max() + 6).reshape(-1, 1)
    future_x_scaled = scaler_x.transform(future_x)
    future_y_scaled = model.predict(future_x_scaled)
    future_y = scaler_y.inverse_transform(future_y_scaled.reshape(-1, 1)).flatten()

    future_data = pd.DataFrame({x_column: future_x.flatten(), y_column: future_y})

    return model, mean_squared_error(y_test_actual, y_pred), r2_score(y_test_actual, y_pred), future_data

# Sidebar UI
st.sidebar.image("images/iesa_white.svg", width=150)
st.sidebar.markdown("<h2>Prediction Engine</h2>", unsafe_allow_html=True)



tables = fetch_tables()
selected_table = st.sidebar.selectbox("Select Table", tables)

if selected_table:
    data = fetch_table_data(selected_table)
    x_column = st.sidebar.selectbox("Select X Column", data.columns)
    y_column = st.sidebar.selectbox("Select Y Column", data.columns)

    run_lr = st.sidebar.button("Run Linear Regression")
    run_pr = st.sidebar.button("Run Polynomial Regression")
    run_rf = st.sidebar.button("Run Random Forest Regression")
    run_svr = st.sidebar.button("Run Support Vector Regression")

    # Execute Regression Based on Button Click
    if run_lr and x_column and y_column:
        model, mse, r2, future_data = perform_linear_regression(data, x_column, y_column)
        st.session_state.results.append({
            "type": "Linear",
            "mse": mse,
            "r2": r2,
            "x_column": x_column,
            "y_column": y_column,
            "data": data.copy(),
            "future_data": future_data.copy()
        })

    if run_pr and x_column and y_column:
        model, poly, mse, r2, future_data = perform_polynomial_regression(data, x_column, y_column)
        st.session_state.results.append({
            "type": "Polynomial",
            "mse": mse,
            "r2": r2,
            "x_column": x_column,
            "y_column": y_column,
            "data": data.copy(),
            "future_data": future_data.copy()
        })

    if run_rf and x_column and y_column:
        model, mse, r2, future_data = perform_random_forest_regression(data, x_column, y_column)
        st.session_state.results.append({
            "type": "Random Forest",
            "mse": mse,
            "r2": r2,
            "x_column": x_column,
            "y_column": y_column,
            "data": data.copy(),
            "future_data": future_data.copy()
        })

    if run_svr and x_column and y_column:
        model, mse, r2, future_data = perform_svr(data, x_column, y_column)
        st.session_state.results.append({
            "type": "SVR",
            "mse": mse,
            "r2": r2,
            "x_column": x_column,
            "y_column": y_column,
            "data": data.copy(),
            "future_data": future_data.copy()
        })

# Display Results
if st.session_state.get("results"):
    col1, col2 = st.columns(2)
    for index, result in enumerate(st.session_state.results):
        with (col1 if index % 2 == 0 else col2):
            actual_chart = alt.Chart(result["data"]).mark_line().encode(
                x=alt.X(result["x_column"], title=result["x_column"]),
                y=alt.Y(result["y_column"], title=result["y_column"]),
                color=alt.value('blue'),
                tooltip=[result["x_column"], result["y_column"]]
            ).properties(title=f'{result["type"]} Regression', width=500, height=350)

            prediction_chart = alt.Chart(result["future_data"]).mark_line(color='red').encode(
                x=alt.X(result["x_column"], title=result["x_column"]),
                y=alt.Y(result["y_column"], title=result["y_column"]),
                tooltip=[result["x_column"], result["y_column"]]
            ).properties(width=500, height=350)

            st.altair_chart(actual_chart + prediction_chart, use_container_width=True)
            st.markdown(f"**MSE:** `{result['mse']:.4f}`  |  **R² Score:** `{result['r2']:.4f}`")
