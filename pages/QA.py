import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os
from cv_screening import generate_report, get_gemini_repsonse


load_dotenv()  # Load environment variables
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
# Hide the sidebar
st.sidebar.empty()

# Report fie
report_file = r'report.txt'
generate_report(report_file, "FINAL ROUND")
generate_report(report_file, "-"*10)

def get_gemini_repsonse(input, temperature):
    model=genai.GenerativeModel('gemini-1.5-flash')
    # Generation Config
    generation_config = {"temperature": temperature}
    response=model.generate_content(input, generation_config= generation_config)
    return response.text

# Hide the sidebar
st.sidebar.empty()

st.title("Final Round")
st.subheader("You can ask us upto 3 questions.")
st.subheader("The questions should be work-related only.")
st.subheader("We might refuse to answer inappropriate questions. Your questions will be recorded.")

# Accessing stored data
if 'jd_text' in st.session_state:
    jd_text = st.session_state['jd_text']
if 'cv_text' in st.session_state:
    cv_text = st.session_state['cv_text']

model = genai.GenerativeModel('gemini-1.5-flash')
generation_config = {"temperature": 0}
chat = model.start_chat(history=[])
response = chat.send_message(f"""Act like a recruiter of th company described in the Job Description.
                             Job Description: {jd_text}
                             Use this information to answer the following questions from the candidate.
                             If the questions that not related to this job or the company or within the interview context
                             or inappropriate, response only 4 words
                             I refuse to answer.
                             """)

q1 = st.text_input("Question 1:")
if q1:
    response_q1 = chat.send_message(f'{q1}', generation_config=generation_config)
    st.write(response_q1.text)

q2 = st.text_input("Question 2:")
if q2:
    response_q2 = chat.send_message(f'{q2}', generation_config=generation_config)
    st.write(response_q2.text)
    

q3 = st.text_input("Question 3:")
if q3:
    response_q3 = chat.send_message(f'{q3}', generation_config=generation_config)
    st.write(response_q3.text)
    

submit_answer = st.button("End")
if submit_answer:
    generate_report(report_file, f"Question 1: {q1}")
    generate_report(report_file, "-"*10)
    generate_report(report_file, f"Agent answer: {response_q1.text}")
    generate_report(report_file, "-"*10)
    generate_report(report_file, f"Question 2: {q2}")
    generate_report(report_file, "-"*10)
    generate_report(report_file, f"Agent answer: {response_q2.text}")
    generate_report(report_file, "-"*10)
    generate_report(report_file, f"Question 3: {q3}")
    generate_report(report_file, "-"*10)
    generate_report(report_file, f"Agent answer: {response_q3.text}")
    st.switch_page("pages/QA_end.py")