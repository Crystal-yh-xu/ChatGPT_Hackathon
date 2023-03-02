import streamlit as st
import snowflake.connector
import openai
import pandas as pd
from PIL import Image
import os
from dotenv import load_dotenv

# pip install dependent libraries 
load_dotenv()

# Set up OpenAI API credentials
openai.api_key = os.getenv('OPENAI_API_KEY')

# Set up Snowflake credentials
account = os.getenv('SNOWFLAKE_ACCOUNT')
user = os.getenv('SNOWFLAKE_USER')
password = os.getenv('SNOWFLAKE_PASSWORD')
warehouse = os.getenv('SNOWFLAKE_WAREHOUSE')
database = os.getenv('SNOWFLAKE_DATABASE')
schema = os.getenv('SNOWFLAKE_SCHEMA')

# Connect to Snowflake database
conn = snowflake.connector.connect(
    user=user,
    password=password,
    account=account,
    warehouse=warehouse,
    database=database,
    schema=schema
)

# Function to generate SQL queries from natural language input
def generate_sql(query):
    response = openai.Completion.create(
        model="code-davinci-002",
        prompt="### Snowflake SQL tables, with their properties:\n#\n# EMPLOYEES(EMPLOYEE_ID, FIRST_NAME, LAST_NAME, DISPLAY_NAME)\n# HOSPITALS(HOSPITAL_ID, HOSPITAL_NAME)\n# WARDS(WARD_ID, WARD_NAME)\n# TAGS(TAG_ID, TAG_NAME)\n# SHIFT_TYPE(SHIFT_TYPE_ID, SHIFT_NAME, SHIFT_START_TIME)\n# SHIFTS(SHIFT_DATE, HOSPITAL_ID, WARD_ID, SHIFT, SHIFT_TYPE_ID, START_DT, END_DT, EMPLOYEE_ID, TAG_ID)\n# INVENTORY_TYPE(INVENTORY_TYPE_ID, NAME, DESCRIPTION)\n# INVENTORY(INVENTORY_ID, INVENTORY_TYPE_ID, COMMISSIONED_DATE, IS_RETIRED)\n# PATIENTS(PATIENT_ID, NAME)\n# INVENTORY_ASSIGNMENTS(ASSIGNMENT_ID, INVENTORY_ID, PATIENT_ID, ASSIGNED_DATETIME, HOSPITAL_ID, WARD_ID, ASSIGNED_BY)\n#\n### A query to "+query+"\nSELECT",
        temperature=0,
        max_tokens=1024,
        top_p=1,
        frequency_penalty=0.0,
        presence_penalty=0,
        stop=["#", ";"],
    )

    sql_query = response.choices[0].text.strip() # re.findall(r"SELECT.*?;", response.choices[0].text.strip(), re.DOTALL)
    return "SELECT "+sql_query+";"

# Create a function to generate next best action recommendations
def generate_recommendations(query):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt="Act as a Next Best Action recommendation engine. Some just ask you about \""+query+"\". The response was positive. What should be the next action recommendation questions from you? Give 5 questions.",
        temperature=0.8,
        max_tokens=1024,
        top_p=1,
        frequency_penalty=0.0,
        presence_penalty=0,
    )
    recommendations = response.choices[0].text
    return recommendations

# Create a function to retrieve data from Snowflake using a SQL query
def get_data(sql_query):
    data = pd.read_sql_query(sql_query, conn)
    return data

# Create a function to execute SQL query
def execute_sql_query(query, sql_query):
    try:
        data = get_data(sql_query)
        if data.empty:
            st.error('There is no data for your query!')
        else:
            with st.expander("See question:"):
                st.write(query)
            with st.expander("See SQL query:"):
                st.write(sql_query)
            # with st.expander("Next best action recommendations:"):
            #     st.write(generate_recommendations(query))
            # Display the data in a table
            st.write("Here's your data:")
            st.table(data)
    except Exception as e:
        st.error('Data extracted unsuccessful! Please describe you question more specific!')

# # Refer the custom CSS styles
def style_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

st.set_page_config(layout='wide')

style_css("style.css")

col1_1, col1_2, col1_3 = st.columns([3,1,3])

# Create the logo
with col1_2:
    logo = Image.open('image/logo.jpg')
    st.image(logo,width=200)

col2_1, col2_2, col2_3, col2_4 = st.columns([3,3,1,2.5])

# Get user input using ChatGPT
with col2_2:
    st.text_input(
        label="Communicate witn your data",
        label_visibility="hidden",
        placeholder="Ask a question about your data: eg. Retrieve all employees",
        value="",
        key="user_input",
    )

with col2_3:
    st.write("")
    st.write("")
    button_search = st.button("Search")

# Example questions
question_01 = "List all shifts which started on 5th Feb 2023 for the hospital named West Port Medical"
question_02 = "Which employee has the most evening shifts between 5th Feb 2023 and 15th Feb 2023"
question_03 = "List all morning shifts belong to employees whose names are Andrew Krotz and Caroline Laurin"
question_04 = "Which hospital has the most shifts between 5th Feb 2023 and 10th Feb 2023"

col3_1, col3_2, col3_3 = st.columns([3,4,2.5])
with col3_2:
    st.write("Popular Questions:")

col4_1, col4_2, col4_3, col4_4, col4_5 = st.columns([3,1.85,1.85,0.8,2])

with col4_2:  
    button_example1 = st.button(question_01)
with col4_3:
    button_example2 = st.button(question_02)

col5_1, col5_2, col5_3, col5_4, col5_5 = st.columns([3,1.85,1.85,0.8,2])
with col5_2:
    button_example3 = st.button(question_03)
with col5_3:
    button_example4 = st.button(question_04)

# Retrieve data from Snowflake using the SQL query
col6_1, col6_2, col6_3 = st.columns([1,3,1])
with col6_2:
    if button_search:
        if st.session_state.user_input == "":
            sql_query = generate_sql("Retrieve all employees")
            execute_sql_query("Retrieve all employees", sql_query)
        else:
            sql_query = generate_sql(st.session_state.user_input)
            execute_sql_query(st.session_state.user_input, sql_query)
    elif button_example1:
        sql_query = generate_sql(question_01)
        execute_sql_query(question_01, sql_query)
    elif button_example2:
        sql_query = generate_sql(question_02)
        execute_sql_query(question_02, sql_query)
    elif button_example3:
        sql_query = generate_sql(question_03)
        execute_sql_query(question_03, sql_query)
    elif button_example4:
        sql_query = generate_sql(question_04)
        execute_sql_query(question_04, sql_query)
    else:
        st.write("")