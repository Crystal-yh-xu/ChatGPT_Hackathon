import streamlit as st
from streamlit_searchbox import st_searchbox
import snowflake.connector
import openai
import pandas as pd
from PIL import Image
import re

# Set up OpenAI API credentials
openai.api_key = "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"

# Set up Snowflake credentials
account = 'gw34330.ap-southeast-2'
user = 'crystal'
password = 'DTT!ChatGPT123'
warehouse = 'compute_wh'
database = 'hackathon'
schema = 'dev'

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
        prompt="### Snowflake SQL tables, with their properties:\n#\n# EMPLOYEES(EMPLOYEE_ID, FIRST_NAME, LAST_NAME, DISPLAY_NAME)\n# HOSPITALS(HOSPITAL_ID, HOSPITAL_NAME)\n# WARDS(WARD_ID, WARD_NAME)\n# TAGS(TAG_ID, TAG_NAME)\n# SHIFT_TYPE(SHIFT_TYPE_ID, SHIFT_NAME, SHIFT_START_TIME)\n# SHIFTS(SHIFT_DATE, HOSPITAL_ID, WARD_ID, SHIFT, SHIFT_TYPE_ID, START_DT, END_DT, EMPLOYEE_ID, TAG_ID)\n#\n### A query to "+query+"\nSELECT",
        #"Generate SQL query to "+query,
        temperature=0,
        max_tokens=1024,
        top_p=1,
        frequency_penalty=0.0,
        presence_penalty=0,
        stop=["#", ";"],
    )

    sql_query = response.choices[0].text.strip() # re.findall(r"SELECT.*?;", response.choices[0].text.strip(), re.DOTALL)
    return "SELECT "+sql_query+";"

# Create a function to retrieve data from Snowflake using a SQL query
def get_data(sql_query):
    data = pd.read_sql_query(sql_query, conn)
    return data

# Create a function to execute SQL query
def execute_sql_query(sql_query):
    try:
        data = get_data(sql_query)
        if data.empty:
            st.error('There is no data for your query!')
        else:
            with st.expander("See SQL query"):
                st.write(sql_query)
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
        label="",
        label_visibility="hidden",
        placeholder="Ask a question about your data: eg. retrieve all employees",
        value="",
        key="user_input",
    )

with col2_3:
    st.write("")
    st.write("")
    button_search = st.button("Search")

col3_1, col3_2, col3_3 = st.columns([3,4,2.5])
with col3_2:
    st.write("Popular Questions:")

col4_1, col4_2, col4_3, col4_4, col4_5 = st.columns([3,1.8,1.8,0.9,2])

with col4_2:  
    button_example1 = st.button("List all shifts which started on 5th Feb 2023 for the hospital named West Port Medical")
with col4_3:
    button_example2 = st.button("Which employee has the most evening shifts between 5th Feb 2023 and 15th Feb 2023")

col5_1, col5_2, col5_3, col5_4, col5_5 = st.columns([3,1.8,1.8,0.9,2])
with col5_2:
    button_example3 = st.button("List all morning shifts which belong to employees whose names are Andrew Krotz and Caroline Laurin")
with col5_3:
    button_example4 = st.button("Which hospital has the most shifts between 5th Feb 2023 and 10th Feb 2023")

# Retrieve data from Snowflake using the SQL query
col6_1, col6_2, col6_3 = st.columns([1,3,1])
with col6_2:
    if button_search:
        if st.session_state.user_input == "":
            sql_query = generate_sql("retrieve all employees")
            execute_sql_query(sql_query)
        else:
            sql_query = generate_sql(st.session_state.user_input)
            execute_sql_query(sql_query)
    elif button_example1:
        sql_query = generate_sql("List all shifts which started on 5th Feb 2023 for the hospital named West Port Medical")
        execute_sql_query(sql_query)
    elif button_example2:
        sql_query = generate_sql("Which employee has the most evening shifts between 5th Feb 2023 and 15th Feb 2023")
        execute_sql_query(sql_query)
    elif button_example3:
        sql_query = generate_sql("List all morning shifts which belong to employees whose names are Andrew Krotz and Caroline Laurin")
        execute_sql_query(sql_query)
    elif button_example4:
        sql_query = generate_sql("Which hospital has the most shifts between 5th Feb 2023 and 10th Feb 2023")
        execute_sql_query(sql_query)
    else:
        st.write("")