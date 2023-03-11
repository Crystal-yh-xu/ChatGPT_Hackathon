import streamlit as st
import snowflake.connector
import openai
import pandas as pd
from PIL import Image
import os
from dotenv import load_dotenv
import speech_recognition as sr
import base64
import re

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

def generate_result(system, assistant, user):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0301",
        messages=[
            {"role": "system", "content": system},
            {"role": "assistant", "content": assistant},
            {"role": "user", "content": user}
        ]
    )
    result = response.choices[0].message.content
    # print(response)
    # print(result)
    return result

# Create a function to generate a SQL query
def generate_sql_query(query):
    system_sql = "You are a SQL query generator."
    assistant_sql= "Snowflake database tables: \ntable EMPLOYEES, columns = [EMPLOYEE_ID, FIRST_NAME, LAST_NAME, DISPLAY_NAME];\ntable HOSPITALS, columns = [HOSPITAL_ID, HOSPITAL_NAME];\ntable WARDS, columns = [WARD_ID, WARD_NAME];\ntable TAGS, columns = [TAG_ID, TAG_NAME];\ntable SHIFT_TYPE, columns = [SHIFT_TYPE_ID, SHIFT_NAME, SHIFT_START_TIME];\ntable SHIFTS, columns = [SHIFT_DATE, HOSPITAL_ID, WARD_ID, SHIFT, SHIFT_TYPE_ID, START_DT, END_DT, EMPLOYEE_ID, TAG_ID];\ntable INVENTORY_TYPE, columns = [INVENTORY_TYPE_ID, NAME, DESCRIPTION];\ntable INVENTORY, columns = [INVENTORY_ID, INVENTORY_TYPE_ID, COMMISSIONED_DATE, IS_RETIRED];\ntable PATIENTS, columns = [PATIENT_ID, NAME];\ntable INVENTORY_ASSIGNMENTS, columns = [ASSIGNMENT_ID, INVENTORY_ID, PATIENT_ID, ASSIGNED_DATETIME, HOSPITAL_ID, WARD_ID, ASSIGNED_BY].\ntable HOSPITALS, column HOSPITAL_NAME contains West Port Medical, Fowler Hospital, Armalch Hospital, Touche Med.\ntable WARDS, column WARD_NAME contains Intensive Care Unit (ICU), Anesthetics, Cardiology, Gastroenterology, General Surgery, Gynecology, Nephrology, Neurology, Occupational Therapy, Ophthalmology, Urology, Renal, Otolaryngology (Ear Nose and Throat), Haematology, Oncology, Orthopaedics, Burn Center (Burn Unit or Burns Unit), Accident and, emergency (A&E), Admissions, Breast Screening, Central Sterile Services Department (CSSD), Chaplaincy, Coronary Care Unit (CCU), Critical Care, Diagnostic Imaging, Elderly Services, Infection Control, Information, Management, Maternity, Microbiology, Neonatal, Nutrition and Dietetics, Obstetrics/Gynecology, Pain Management, Pharmacy, Physiotherapy, Radiology, Radiotherapy, Rheumatology, Sexual Health, Social Work.\ntable TAGS, column Tag_NAME contains consultant, medical emergency, anaesthetist, resuscitation.\ntable SHIFT_TYPE, column SHIFT_NAME contains Morning, Mid, Night.\ntable INVENTORY_TYPE, column NAME contains MRI Machine, X-Ray Machine, Ultrasound Machine, CT Scanner, Infusion Pump, Wheelchair, Stethoscope, Defibrillator, Blood Pressure Monitor, Oxygen Meter, Otoscope, Thermometer, Sphygmomanometer, ECG Machine."
    user_sql = "Based on the provided Snowflake database tables, generate a SQL query to "
    string = generate_result(system_sql, assistant_sql, user_sql+query)
    # Define a regular expression pattern to match SQL statements
    sql_pattern = re.compile(r'\bSELECT\b[\s\S]*?;', re.IGNORECASE)
    # Search the string for SQL statements
    sql_match = sql_pattern.search(string)
    sql_query = sql_match.group().strip()
    return sql_query

# Create a function to generate recommendation questions
def generate_recommendation(query):
    system_recommendation = "You are a Next Best Action recommendation engine."
    assistant_recommendation = "Snowflake database tables: \ntable EMPLOYEES, columns = [EMPLOYEE_ID, FIRST_NAME, LAST_NAME, DISPLAY_NAME];\ntable HOSPITALS, columns = [HOSPITAL_ID, HOSPITAL_NAME];\ntable WARDS, columns = [WARD_ID, WARD_NAME];\ntable TAGS, columns = [TAG_ID, TAG_NAME];\ntable SHIFT_TYPE, columns = [SHIFT_TYPE_ID, SHIFT_NAME, SHIFT_START_TIME];\ntable SHIFTS, columns = [SHIFT_DATE, HOSPITAL_ID, WARD_ID, SHIFT, SHIFT_TYPE_ID, START_DT, END_DT, EMPLOYEE_ID, TAG_ID];\ntable INVENTORY_TYPE, columns = [INVENTORY_TYPE_ID, NAME, DESCRIPTION];\ntable INVENTORY, columns = [INVENTORY_ID, INVENTORY_TYPE_ID, COMMISSIONED_DATE, IS_RETIRED];\ntable PATIENTS, columns = [PATIENT_ID, NAME];\ntable INVENTORY_ASSIGNMENTS, columns = [ASSIGNMENT_ID, INVENTORY_ID, PATIENT_ID, ASSIGNED_DATETIME, HOSPITAL_ID, WARD_ID, ASSIGNED_BY].\ntable HOSPITALS, column HOSPITAL_NAME contains West Port Medical, Fowler Hospital, Armalch Hospital, Touche Med.\ntable WARDS, column WARD_NAME contains Intensive Care Unit (ICU), Anesthetics, Cardiology, Gastroenterology, General Surgery, Gynecology, Nephrology, Neurology, Occupational Therapy, Ophthalmology, Urology, Renal, Otolaryngology (Ear Nose and Throat), Haematology, Oncology, Orthopaedics, Burn Center (Burn Unit or Burns Unit), Accident and, emergency (A&E), Admissions, Breast Screening, Central Sterile Services Department (CSSD), Chaplaincy, Coronary Care Unit (CCU), Critical Care, Diagnostic Imaging, Elderly Services, Infection Control, Information, Management, Maternity, Microbiology, Neonatal, Nutrition and Dietetics, Obstetrics/Gynecology, Pain Management, Pharmacy, Physiotherapy, Radiology, Radiotherapy, Rheumatology, Sexual Health, Social Work.\ntable TAGS, column Tag_NAME contains consultant, medical emergency, anaesthetist, resuscitation.\ntable SHIFT_TYPE, column SHIFT_NAME contains Morning, Mid, Night.\ntable INVENTORY_TYPE, column NAME contains MRI Machine, X-Ray Machine, Ultrasound Machine, CT Scanner, Infusion Pump, Wheelchair, Stethoscope, Defibrillator, Blood Pressure Monitor, Oxygen Meter, Otoscope, Thermometer, Sphygmomanometer, ECG Machine."
    user_recommendation = "Some just ask you about "+query+". The response was positive. What should be the next action recommendation questions from you based on the Snowflake database table information. Give 5 recommendation questions."
    recommendation = generate_result(system_recommendation, assistant_recommendation, user_recommendation)
    return recommendation

# Create a function to generate summary
def generate_summary(query, data):
    system_summary = "You are a summary generator."
    assistant_summary = "Question: "+query+"\nAnswer: "+data.to_string()
    user_ummary  = "Generate a summary based on the provided question and answer"
    summary = generate_result(system_summary, assistant_summary, user_ummary)
    return summary

# Create a function to retrieve data from Snowflake using a SQL query
def get_data(sql_query):
    data = pd.read_sql_query(sql_query, conn)
    return data

# Generate "See question" "See SQL query" "See next best action recommendation questions" and data from Snowflake database when click the button
def execute_query(query, sql_query):
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
                st.caption(generate_recommendation(query))
            # Display the data in a table
            st.write("Here's your data:")
            try:
                st.write(generate_summary(query, data))
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


# Create the logo
col1_1, col1_2, col1_3, col1_4, col1_5, col1_6, col1_7 = st.columns(7)

with col1_4:
    logo = Image.open('image/logo.jpg')
    st.image(logo,width=200)

# Get user input using ChatGPT
col2_1, col2_2, col2_3, col2_4, col2_5 = st.columns([2.2,3,0.58,0.58,2])

with col2_2:
    st.text_input(
        label="Communicate with your data",
        label_visibility="hidden",
        placeholder="Ask a question about your data: eg. Show all hospitals.",
        value="",
        key="user_input",
    )

# Search button
with col2_3:
    st.write("")
    st.write("")
    button_search = st.button("Search")

with col2_4:
    st.write("")
    st.write("")
    button_speak = st.button("Speak")

# Example questions
question_01 = "Is there any wheelchair available in inventory right now?"
question_02 = "Who is currently rostered for general anaesthetic specialty?"
question_03 = "Give me a list of wards that are overstaffed or understaffed this weekend?"
question_04 = "Please generate a 3D model from chest xray scans for the patient Alex in Breast Screening?"
question_05 = "Please generate a discharge summary report for the patient in Ward Intensive Care Unit (ICU)?"
question_06 = "Does the patient in Critical Care ever had any advsere reactions or side effects to any medications?"
question_07 = "Can you provide me with information on the latest evidence-based practices for managing patients with diabetes and suspected streptococcus infection?"
question_08 = "Please generate an ED care plan for Patient Irha Sigler by utilising the triage assessment notes and evaluating the patient's vitals?"
question_09 = "Is there any previous medical history or patient data of Patient Clara Dajani that should be taken into consideration before the surgery?"

col3_1, col3_2, col3_3 = st.columns([2.2,4.16,2])

with col3_2:
    st.write("Popular Questions:")

col4_1, col4_2, col4_3, col4_4, col4_5 = st.columns([2.2,1.3867,1.3867,1.3867,2])

with col4_2:  
    button_example1 = st.button(question_01)
with col4_3:
    button_example2 = st.button(question_02)
with col4_4:
    button_example3 = st.button(question_03)

col5_1, col5_2, col5_3, col5_4, col5_5 = st.columns([2.2,1.3867,1.3867,1.3867,2])
with col5_2:
    button_example4 = st.button(question_04)
with col5_3:
    button_example5 = st.button(question_05)
with col5_4:
    button_example6 = st.button(question_06)

col6_1, col6_2, col6_3, col6_4, col6_5 = st.columns([2.2,1.3867,1.3867,1.3867,2])
with col6_2:
    button_example7 = st.button(question_07)
with col6_3:
    button_example8 = st.button(question_08)
with col6_4:
    button_example9 = st.button(question_09)

# container for generated results
col7_1, col7_2, col7_3 = st.columns([1,3,1])
with col7_2:
    if button_search:
        if st.session_state.user_input == "":
            query_defult = "Show all hospitals."
            sql_query = generate_sql_query(query_defult)
            execute_query(query_defult, sql_query)
        else:
            sql_query = generate_sql_query(st.session_state.user_input)
            execute_query(st.session_state.user_input, sql_query)
    elif button_example1:
        sql_query = generate_sql_query(question_01)
        execute_query(question_01, sql_query)
    elif button_example2:
        with st.expander("See question:"):
            st.caption(question_02)
        with st.expander("See next best action recommendation questions:"):
            st.caption(generate_recommendation(question_02))
    elif button_example3:
        with st.expander("See question:"):
            st.caption(question_03)
        with st.expander("See next best action recommendation questions:"):
            st.caption(generate_recommendation(question_03))
    elif button_example4:
        with st.expander("See question:"):
            st.caption(question_04)
        with st.expander("See next best action recommendation questions:"):
            st.caption(generate_recommendation(question_04))
        st.write("Chest xray scan images and generated 3D models")
        col8_1, col8_2 = st.columns([1,1.75])
        with col8_1:
            image = Image.open('image/lungs_image.jpg')
            st.image(image, caption='', width=327)
        with col8_2:
            ### gif from local file
            gif_path = 'image/3d_lungs.gif'
            file_ = open(gif_path, "rb")
            contents = file_.read()
            data_url = base64.b64encode(contents).decode("utf-8")
            file_.close()
            st.markdown(
                f'<img src="data:image/gif;base64,{data_url}" alt="cat gif">',
                unsafe_allow_html=True,
            )
    elif button_example5:
        with st.expander("See question:"):
            st.caption(question_05)
        with st.expander("See next best action recommendation questions:"):
            st.caption(generate_recommendation(question_05))
    elif button_example6:
        with st.expander("See question:"):
            st.caption(question_06)
        with st.expander("See next best action recommendation questions:"):
            st.caption(generate_recommendation(question_06))
    elif button_example7:
        with st.expander("See question:"):
            st.caption(question_07)
        with st.expander("See next best action recommendation questions:"):
            st.caption(generate_recommendation(question_07))
    elif button_example8:
        with st.expander("See question:"):
            st.caption(question_08)
        with st.expander("See next best action recommendation questions:"):
            st.caption(generate_recommendation(question_08))
    elif button_example9:
        with st.expander("See question:"):
            st.caption(question_09)
        with st.expander("See next best action recommendation questions:"):
            st.caption(generate_recommendation(question_09))
    # Speech to Text
    elif button_speak:
        with st.empty():
            st.write('Listening...')
            # Set up a speech recognizer object
            r = sr.Recognizer()
            # Start listening to the user's microphone input
            with sr.Microphone() as source:
                audio = r.listen(source)
            # Convert the speech to text using the Google Speech Recognition API
            speech = r.recognize_google(audio)
            # text = openai.Audio.transcribe("whisper-1", audio)
            # Display the converted text in a text area
            st.write('Speech to Text...')
        with st.expander("See question:"):
            st.caption(speech)
        with st.expander("See next best action recommendation questions:"):
            st.caption(generate_recommendation(speech))
    else:
        st.empty()



st.write("")
st.write("")
st.write("")
st.write("")
st.write("")
st.write("")
st.write("")
st.write("")
st.write("")
st.write("")

# Footer

col9_1, col9_2, col9_3  = st.columns([5,1,5])
with col9_2:
    st.caption("🚨"+"Caution Message"+"🚨")

col10_1, col10_2, col10_3 = st.columns([2.2,4.16,2])
with col10_2:
    st.caption("Please be aware that while the app is designed to assist medical decision-making and check symptoms, the final diagnosis should be made by a licensed medical professional. We recommend seeking additional evaluations and opinions before making any treatment decisions.")