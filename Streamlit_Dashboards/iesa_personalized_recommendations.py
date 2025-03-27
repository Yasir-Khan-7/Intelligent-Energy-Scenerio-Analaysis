import streamlit as st
import asyncio
import pandas as pd
import mysql.connector
from pydantic_ai import Agent
from pydantic_ai.models.groq import GroqModel
import random

st.set_page_config(page_title="IESA Dashboard", layout="wide", page_icon="📊")

# Local image path (Replace with your actual image path)
image_path = "images/iesa_green.svg"
# Load logo

# Apply Custom CSS for Chat Styling
st.markdown(
    """
    <style>
    header {
        border-bottom: 3px solid  #136a8a !important; 
    }
    [data-testid="stSidebar"] {
        background: linear-gradient(135deg, #73C8A9, #0b8793); /* Gradient background */
        color: white;
        margin-top:58px;
        box-shadow: 2px 0 10px rgba(0,0,0,0.2);
    }

    [data-testid="stSidebar"]
    .sidebar-content {
        margin-top: -60px;
        padding: 20px;
    }
     [data-testid="stSidebarHeader"]{
     display: none;
     }
     h1{
     font-size: 32px !important;
     margin-top: 10px !important;
     text-align: center;
     text-shadow: 1px 1px 2px rgba(0,0,0,0.2);
     letter-spacing: 0.5px;
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
    
    
    [data-testid="stSidebar"] h2 {
        font-size: 22px !important;
        margin-top: 25px !important;
        margin-bottom: 15px !important;
        padding-bottom: 5px;
        border-bottom: 2px solid rgba(255,255,255,0.3);
        text-shadow: 1px 1px 2px rgba(0,0,0,0.2);
    }
    
    [data-testid="stSidebar"] p {
        color: rgba(255,255,255,0.9) !important;
        font-weight: 500;
        margin-bottom: 8px;
    }
    
    [data-testid="stSidebar"] label {
        color: white !important;
        font-weight: 500;
        font-size: 15px;
        margin-bottom: 5px;
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
    
    [data-testid="stBaseButton-secondary"]{
            
            background-color: #0b8793 !important;
             width:100% !important;
             border: 1px solid #4AC29A;
            border-radius: 5px;
            }

      [data-testid="stBaseButton-secondary"]:hover {
        background-color: #0b8793;
        color: white !important;
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
    
    .chat-container {
        display: flex;
        flex-direction: column;
        gap: 10px;
        padding: 10px;
    }
    .user-container {
        display: flex;
        align-content: flex-end;
        justify-content: flex-end;
        align-items: flex-end;
        font-size: 15px;
    }
    .bot-container {
        font-size: 15px;
    }
    .user-msg {
        width: fit-content;
        background-color: #e9f5ff;
        color: #222;
        padding: 12px 18px;
        border-radius: 18px 18px 0 18px;
        text-align: right;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        border: 1px solid #c9e6ff;
        font-weight: 500;
        letter-spacing: 0.2px;
        line-height: 1.4;
    }
    .bot-msg {
        width: fit-content;
        background-color: #f8f0e5;
        color: #222;
        padding: 12px 18px;
        border-radius: 18px 18px 18px 0;
        text-align: left;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        border: 1px solid #f1e2cc;
        font-weight: 500;
        letter-spacing: 0.2px;
        line-height: 1.4;
    }
    .chat-header {
        text-align: center;
        font-size: 24px;
        font-weight: bold;
        margin-bottom: 10px;
    }
    .chat-description {
        text-align: center;
        color: gray;
        font-size: 14px;
        margin-bottom: 20px;
    }
    [data-baseweb="textarea"] {
        border: 2px solid #0b8793 !important;
        border-radius: 25px !important;
        background-color: white !important;
        box-shadow: 0 2px 6px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
    }
    
    [data-baseweb="textarea"]:focus-within {
        border-color: #4AC29A !important;
        box-shadow: 0 3px 10px rgba(0,0,0,0.15);
    }
    
    textarea[aria-label="Type your message..."] {
        padding: 12px !important;
        font-size: 16px !important;
    }
    
    textarea[aria-label="Type your message..."]::placeholder {
        color: #666 !important; 
        font-weight: 500;
    }
    
    [data-testid="stChatInput"] {
        margin: 15px 0;
        padding-bottom: 10px;
    }
    
    [data-testid="stChatInputSubmitButton"] {
        background-color: #0b8793 !important;
        color: white !important;
        border-radius: 50%;
        margin-right: 5px;
        transition: all 0.2s ease;
        transform: translateY(4px);
        margin-bottom: 8px;
    }
    
    [data-testid="stChatInputSubmitButton"]:hover {
        background-color: #4AC29A !important;
        transform: translateY(4px) scale(1.05);
    }
    
    [data-testid="stChatInputContainer"] {
        padding-right: 10px;
    }
    
    [data-testid="stFullScreenFrame"]{
        display: flex;
        align-content: center;
        justify-content: center;
    }
    
    </style>
    """,
    unsafe_allow_html=True,
)

api_keys = [
    "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",  
    "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",
    "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",
    "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"
]

api_index = 0

def get_model():
    global api_index
    for _ in range(len(api_keys)):
        api_key = api_keys[api_index]
        api_index = (api_index + 1) % len(api_keys)
        try:
            return GroqModel('qwen-2.5-32b', api_key=api_key)
        except Exception:
            continue
    return None

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        port="3306",
        user="root",
        passwd="admin123",
        db="iesa_db"
    )

def fetch_tables():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SHOW TABLES")
        tables = [table[0] for table in cursor.fetchall() if table[0] != "user_data"]
        conn.close()
        return tables
    except Exception as e:
        st.error(f"Error fetching tables: {e}")
        return []

def fetch_table_data(table_name):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        query = f"SELECT * FROM {table_name}"
        cursor.execute(query)
        rows = cursor.fetchall()
        data = pd.DataFrame(rows, columns=[desc[0] for desc in cursor.description])
        conn.close()
        return data
    except Exception as e:
        st.error(f"Error fetching data from {table_name}: {e}")
        return pd.DataFrame()

# Fetch scenario categories
def fetch_scenario_categories():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT category FROM scenario_definitions")
        categories = [row[0] for row in cursor.fetchall()]
        conn.close()
        return categories
    except Exception as e:
        st.error(f"Error fetching scenario categories: {e}")
        return []

# Fetch scenarios based on selected category
def fetch_scenarios(category):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        query = "SELECT scenario FROM scenario_definitions WHERE category = %s"
        cursor.execute(query, (category,))
        scenarios = [row[0] for row in cursor.fetchall()]
        conn.close()
        return scenarios
    except Exception as e:
        st.error(f"Error fetching scenarios: {e}")
        return []

st.sidebar.markdown("""
    <h1>IESA Assistant</h1>
""",unsafe_allow_html=True)
# Sidebar UI for scenario selection
st.sidebar.header("Table Selection")
# Add sidebar with table selection and action buttons
tables = fetch_tables()
selected_table = st.sidebar.selectbox("Select a Table", tables)


if "knowledge_base" not in st.session_state:
    st.session_state.knowledge_base = ""
    tables = fetch_tables()
    for table in tables:
        data = fetch_table_data(table)
        st.session_state.knowledge_base += f"\nTable: {table}\n{data.to_string(index=False)}\n"

if "conversation_history" not in st.session_state:
    st.session_state.conversation_history = []



async def get_response(user_input):
    st.session_state.conversation_history.append({"role": "user", "content": user_input})

    last_message = st.session_state.conversation_history[-1]  # Keep only the last user input

    for _ in range(len(api_keys)):
        model = get_model()
        if model:
            try:
                agent = Agent(model=model)
                
                # Only use the last user message while keeping the full knowledge base
                conversation_text = f"User: {last_message['content']}"

                prompt = """🔹 IESA AI Assistant: Provide energy-saving recommendations based on the user's query.
                Suggest cost-effective strategies even if no cost data is available.
                Consider solar panels, battery storage, and demand-side management as options"""

                result = await agent.run(prompt + "\n" + st.session_state.knowledge_base + "\n" + conversation_text)
                response = result.data
                st.session_state.conversation_history.append({"role": "assistant", "content": response})
                return response

            except Exception as e:
                st.warning(f"API call failed, switching API key... ({e})")
                await asyncio.sleep(5)  # Wait before switching API key

    return "Sorry, all API keys failed. Please try again later."
st.image(image_path,width=160)

st.markdown(
    "<p style='text-align: center; color: #666; font-size: 18px; font-weight: 600; margin: 15px 0; line-height: 1.5;'>Your Intelligent Energy Scenario Analysis (IESA) assistant.<br>"
    "Analyze energy consumption, explore future scenarios, and receive personalized recommendations.</p>",
    unsafe_allow_html=True,
)

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    role_class = "user-msg" if message["role"] == "user" else "bot-msg"
    container_class = "user-container" if message["role"] == "user" else "bot-container"
    icon = "💬" if message["role"] == "user" else "⚡"
    st.markdown(
        f'<div class="chat-container {container_class}"><div class="{role_class}">{icon} {message["content"]}</div></div>',
        unsafe_allow_html=True
    )

user_input = st.chat_input("Type your message...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.spinner("Thinking..."):
        bot_reply = asyncio.run(get_response(user_input))
    st.session_state.messages.append({"role": "assistant", "content": bot_reply})
    st.rerun()


# Define buttons and actions
buttons = ["View Data", "Analyze Trends", "Generate Report"]
for btn in buttons:
    if st.sidebar.button(btn):
        user_input = f"{selected_table} - {btn}"
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.spinner("Thinking..."):
            bot_reply = asyncio.run(get_response(user_input))
        st.session_state.messages.append({"role": "assistant", "content": bot_reply})
        st.rerun()

# Sidebar UI for scenario selection
st.sidebar.header("Scenario Selection")

categories = fetch_scenario_categories()
selected_category = st.sidebar.selectbox("Select Category", categories)

if selected_category:
    scenarios = fetch_scenarios(selected_category)
    selected_scenario = st.sidebar.selectbox("Select Scenario", scenarios)

    # Display buttons for actions
    if selected_scenario:
        

        if st.sidebar.button("Generate Recommendation", key=f"rec_{selected_scenario}"):
            user_input = f"Generate recommendation for {selected_scenario}"
            st.session_state.messages.append({"role": "user", "content": user_input})
            with st.spinner("Thinking..."):
                bot_reply = asyncio.run(get_response(user_input))
            st.session_state.messages.append({"role": "assistant", "content": bot_reply})
            st.rerun()

        if st.sidebar.button("Analyze Trends", key=f"trends_{selected_scenario}"):
            user_input = f"Analyze trends for {selected_scenario}"
            st.session_state.messages.append({"role": "user", "content": user_input})
            with st.spinner("Thinking..."):
                bot_reply = asyncio.run(get_response(user_input))
            st.session_state.messages.append({"role": "assistant", "content": bot_reply})
            st.rerun()

        if st.sidebar.button("Generate Report", key=f"report_{selected_scenario}"):
            user_input = f"Generate report for {selected_scenario}"
            st.session_state.messages.append({"role": "user", "content": user_input})
            with st.spinner("Generating report..."):
                bot_reply = asyncio.run(get_response(user_input))
            st.session_state.messages.append({"role": "assistant", "content": bot_reply})
            st.rerun()