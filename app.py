import streamlit as st
import snowflake.connector
import openai
import pandas as pd
from PIL import Image
import os
from dotenv import load_dotenv
import speech_recognition as sr

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
def generate_result(query):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=query,
        temperature=0.5,
        max_tokens=1024,
        top_p=1,
        frequency_penalty=0.2,
        presence_penalty=0
    )

    result = response.choices[0].text.strip() # re.findall(r"SELECT.*?;", response.choices[0].text.strip(), re.DOTALL)
    print(response)
    return result

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
                st.caption(query)
            with st.expander("See SQL query:"):
                st.caption(sql_query)
            with st.expander("See next best action recommendation questions:"):
                st.caption(generate_result("Act as a Next Best Action recommendation engine. Some just ask you about "+query+". The response was positive. What should be the next action recommendation questions from you based on the below table information? \ntable EMPLOYEES, columns = [EMPLOYEE_ID, FIRST_NAME, LAST_NAME, DISPLAY_NAME];\ntable HOSPITALS, columns = [HOSPITAL_ID, HOSPITAL_NAME];\ntable WARDS, columns = [WARD_ID, WARD_NAME];\ntable TAGS, columns = [TAG_ID, TAG_NAME];\ntable SHIFT_TYPE, columns = [SHIFT_TYPE_ID, SHIFT_NAME, SHIFT_START_TIME];\ntable SHIFTS, columns = [SHIFT_DATE, HOSPITAL_ID, WARD_ID, SHIFT, SHIFT_TYPE_ID, START_DT, END_DT, EMPLOYEE_ID, TAG_ID];\ntable INVENTORY_TYPE, columns = [INVENTORY_TYPE_ID, NAME, DESCRIPTION];\ntable INVENTORY, columns = [INVENTORY_ID, INVENTORY_TYPE_ID, COMMISSIONED_DATE, IS_RETIRED];\ntable PATIENTS, columns = [PATIENT_ID, NAME];\ntable INVENTORY_ASSIGNMENTS, columns = [ASSIGNMENT_ID, INVENTORY_ID, PATIENT_ID, ASSIGNED_DATETIME, HOSPITAL_ID, WARD_ID, ASSIGNED_BY]\n#Give 5 questions."))
            # Display the data in a table
            st.write("Here's your data:")
            try: 
                st.write(generate_result("Generate a summary of question: "+query+"and answer below:\n"+data.to_string()))
            except:
                pass
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
        placeholder="Ask a question about your data: eg. Show all employees\' data",
        value="",
        key="user_input",
    )

with col2_3:
    st.write("")
    st.write("")
    button_search = st.button("Search")

# # Speech to Text
# col10_1, col10_2, col10_3 = st.columns([3,4,2.5])
# with col10_2:    
#     if st.button('Convert speech to text'):
#         st.write('Listening...')
#         # Set up a speech recognizer object
#         r = sr.Recognizer()
#         # Start listening to the user's microphone input
#         with sr.Microphone() as source:
#             audio = r.listen(source)
#         # Convert the speech to text using the Google Speech Recognition API
#         text = r.recognize_google(audio)
#         # text = openai.Audio.transcribe("whisper-1", audio)
#         # Display the converted text in a text area
#         st.text_area('Converted text', value=text)

# Example questions
question_01 = "Is there any wheelchair available right now?"
question_02 = "Who is currently rostered for general anaesthetic specialty?"
question_03 = "Please generate a 3D model from chest xray scans for the patient in in ward Breast Screening?"
question_04 = "Please generate a discharge summary report for the patient in Ward Intensive Care Unit (ICU)?"
question_05 = "Give me a list of wards that are overstaffed or understaffed this weekend?"
question_06 = "Does the patient in Critical Care ever had any advsere reactions or side effects to any medications?"
question_07 = "Can you provide me with information on the latest evidence-based practices for managing patients with diabetes and suspected streptococcus infection?"
question_08 = "Please generate an ED care plan for Patient Irha Sigler by utilising the triage assessment notes and evaluating the patient's vitals?"

col3_1, col3_2, col3_3 = st.columns([3,4,2.5])
with col3_2:
    st.write("Popular Questions:")

# col4_1, col4_2, col4_3, col4_4, col4_5, col4_6, = st.columns([2,1.5,1.5,1.5,1.5,2])
col4_1, col4_2, col4_3, col4_4, col4_5 = st.columns([3,1.85,1.85,0.8,2])
with col4_2:  
    button_example1 = st.button(question_01)
with col4_3:
    button_example2 = st.button(question_02)
with col4_2:
    button_example3 = st.button(question_03)
with col4_3:
    button_example4 = st.button(question_04)

# col5_1, col5_2, col5_3, col5_4, col5_5, col5_6 = st.columns([2,1.5,1.5,1.5,1.5,2])
col5_1, col5_2, col5_3, col5_4, col5_5 = st.columns([3,1.85,1.85,0.8,2])
with col5_2:
    button_example5 = st.button(question_05)
with col5_3:
    button_example6 = st.button(question_06)
with col5_2:
    button_example5 = st.button(question_07)
with col5_3:
    button_example6 = st.button(question_08)

# Retrieve data from Snowflake using the SQL query
table_comment = "# Snowflake tables:\n# table EMPLOYEES, columns = [EMPLOYEE_ID, FIRST_NAME, LAST_NAME, DISPLAY_NAME];\n# table HOSPITALS, columns = [HOSPITAL_ID, HOSPITAL_NAME];\n# table WARDS, columns = [WARD_ID, WARD_NAME];\n# table TAGS, columns = [TAG_ID, TAG_NAME];\n# table SHIFT_TYPE, columns = [SHIFT_TYPE_ID, SHIFT_NAME, SHIFT_START_TIME];\n# table SHIFTS, columns = [SHIFT_DATE, HOSPITAL_ID, WARD_ID, SHIFT, SHIFT_TYPE_ID, START_DT, END_DT, EMPLOYEE_ID, TAG_ID];\n# table INVENTORY_TYPE, columns = [INVENTORY_TYPE_ID, NAME, DESCRIPTION];\n# table INVENTORY, columns = [INVENTORY_ID, INVENTORY_TYPE_ID, COMMISSIONED_DATE, IS_RETIRED];\n# table PATIENTS, columns = [PATIENT_ID, NAME];\n# table INVENTORY_ASSIGNMENTS, columns = [ASSIGNMENT_ID, INVENTORY_ID, PATIENT_ID, ASSIGNED_DATETIME, HOSPITAL_ID, WARD_ID, ASSIGNED_BY]\n# Generate a SQL query to "
col6_1, col6_2, col6_3 = st.columns([1,3,1])
with col6_2:
    if button_search:
        if st.session_state.user_input == "":
            sql_query = generate_result(table_comment+"Show all employees' data")
            execute_sql_query("Show all employees' data", sql_query)
        else:
            sql_query = generate_result(table_comment+st.session_state.user_input)
            execute_sql_query(st.session_state.user_input, sql_query)
    elif button_example1:
        sql_query = generate_result(table_comment+question_01)
        execute_sql_query(question_01, sql_query)
    elif button_example3:
        with st.expander("See question:"):
            st.caption(question_03)
        st.write("Chest xray scan images and generated 3D models")
        col8_1, col8_2 = st.columns([1,1])
        with col8_1:
            image = Image.open('image/lungs_image.jpg')
            st.image(image, caption='', use_column_width=True)
        with col8_2:
            video_file = open('image/3d_lungs.mp4', 'rb')
            video_bytes = video_file.read()
            st.video(video_bytes)
    # elif button_example4:
    #     sql_query = generate_result(table_comment+question_04)
    #     execute_sql_query(question_04, sql_query)  
    else:
        st.write("")