import streamlit as st
import snowflake.connector
import openai
import pandas as pd

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
        model="text-davinci-003",
        prompt="Generate a SQL query to " + query,
        temperature=0,
        max_tokens=1024,
        top_p=1,
        frequency_penalty=0.2,
        presence_penalty=0,
    )

    sql_query = response.choices[0].text.strip()
    return sql_query

# Create a function to retrieve data from Snowflake using a SQL query
def get_data(sql_query):
    data = pd.read_sql_query(sql_query, conn)
    return data

# Create a function to execute SQL query
def execute_sql_query(sql_query):
    try:
        data = get_data(sql_query)
        if data.empty:
            st.write('There is no data for your query! Please describe you question more specific!')
        else:
            # Display the data in a table
            st.write("Here's your data:")
            st.table(data)
    except Exception as e:
        st.write('Data extracted unsuccessful! Please describe you question more specific!')

# Create the Streamlit application
st.title("Communication with your data")

# Get user input using ChatGPT
user_input = st.text_input("Ask a question about your data: (eg. retrieve all employees)", value="")

# Generate a SQL query from the user's input
sql_query = generate_sql(user_input)

# Retrieve data from Snowflake using the SQL query
if st.button("Generate"):
    execute_sql_query(sql_query)
