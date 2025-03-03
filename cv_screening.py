import streamlit as st
import google.generativeai as genai
import os
import PyPDF2 as pdf
from dotenv import load_dotenv
from langdetect import detect
import logging
import numpy as np
import re
import nltk
from nltk.corpus import stopwords


load_dotenv() ## load all our environment variables

genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

def input_pdf_text(uploaded_file):
    reader=pdf.PdfReader(uploaded_file)
    text=""
    for page in range(len(reader.pages)):
        page=reader.pages[page]
        text+=str(page.extract_text())
    return text

def generate_report(report_path, content):
    """
    Generates a report by appending content to a file with a newline.

    Args:
        report_path: The path to the report file.
        content: The string content to be added to the report.
    """
    try:
        # Open the file in append mode (creates if it doesn't exist)
        with open(report_path, "a", encoding="utf-8") as file:
            # Write content with a newline character
            file.write(f"{content}\n")
    except (IOError, OSError) as e:  # Catch broader file-related errors
        print(f"Error writing report: {e}")

# Function to preprocess text
def preprocess_text(text):
    # Lowercase
    text = text.lower()
    # Remove punctuation and special characters using regex
    text = re.sub(r'[^\w\s]', '', text)
    # Tokenize using NLTK
    tokens = nltk.word_tokenize(text)
    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    tokens = [token for token in tokens if token not in stop_words]
    # Convert tokens back to string
    preprocessed_text = ' '.join(tokens)
    return preprocessed_text

    
def get_gemini_repsonse(input, temperature):
    model=genai.GenerativeModel('gemini-1.5-flash')
    # Generation Config
    generation_config = {"temperature": temperature}
    response=model.generate_content(input, generation_config= generation_config)
    return response.text

# Get the directory of the script
script_dir = os.path.dirname(os.path.realpath(__file__))
report_file = os.path.join(script_dir, 'report.txt')
log_file = os.path.join(script_dir, 'program_log_cv_screening.txt')

# Create a custom date format for the initial timestamp
date_format = '%d-%m-%Y %H:%M:%S'

# Configure logging to store logs in the script's directory with the custom date format
logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', datefmt=date_format)

# Define variables
cv_text = None
cv_language = None
ai_jd = None
cv_matching_threshold = 50
cv_round_pass = None

# Streamlit app display
st.sidebar.empty() # Hide the sidebar

st.text("Author: Luke Do")
st.header("CV Screening Round")

jd_uploaded_file = st.file_uploader("Upload Job Description",type="pdf",help="Please upload the pdf")
cv_uploaded_file = st.file_uploader("Upload Candidate CV",type="pdf",help="Please upload the pdf")

cand_first_name = st.text_input("Please enter your first name")
cand_last_name = st.text_input("Please enter your last name")
cand_email = st.text_input("Please enter your email")
check_cv = st.button("Check CV")

try:
    if check_cv:
        logging.info(f"---------------{cand_first_name} {cand_last_name} Program log------------------")
        generate_report(report_file, f"FEEDBACK REPORT of {cand_first_name} {cand_last_name}")
        generate_report(report_file, "-"*10)
        logging.info("-"*10)
        logging.info("Uploading CV")
        logging.info("-"*10)
        if cv_uploaded_file is not None and jd_uploaded_file is not None:
            logging.info("CV uploaded successfully")
            logging.info("-"*10)
            logging.info("Detecting language")
            # Extract text from CV and detect language and store cv_language in session
            cv_text = input_pdf_text(cv_uploaded_file)
            cv_language = detect(cv_text)
            st.session_state['cv_language'] = cv_language
            
            # Extract text from JD and detect language and store jd_lang in session
            jd_text = input_pdf_text(jd_uploaded_file)
            jd_lang = detect(jd_text)
            st.session_state['jd_lang'] = jd_lang
            
            generate_report(report_file, "Checking Language")
            logging.info("-"*10)
            # Logic 1: If language of CV is not English, reject the candidate
            if cv_language != jd_lang:
                generate_report(report_file, "This candidate is not eligible due to CV not match the requried language")
                generate_report(report_file, "-"*10)
                st.switch_page("pages/cv_screening_feedback.py")
            else:   
                generate_report(report_file, "This candidate matched the requried language")
                generate_report(report_file, "-"*10)

                # Preprocess texts
                logging.info("Preprocessing Text")
                preprocessed_jd_text = preprocess_text(jd_text)
                preprocessed_cv_text = preprocess_text(cv_text)
                logging.info("Preprocessed Text Sucessfully")
                logging.info("-"*10)

                prompt = f"""
                    Act Like a skilled or very experience ATS(Application Tracking System)
                    with a deep understanding of tech field,software engineering,data science ,data analyst
                    and big data engineer. Your task is to evaluate the resume based on the given job description.
                    You must consider the job market is very competitive and you should provide 
                    best assistance for improving thr resumes. Assign the percentage Matching based 
                    on Jd and the missing keywords with high accuracy
                    resume:{preprocessed_cv_text}
                    description:{preprocessed_jd_text}

                    I want the response have a structure of 3 lines. 
                    JD Match Score: (scale 0-100) not percentage
                    Profile Summary: (max 50 words)
                    Missing Skills:
                    """
                logging.info("Sending prompt to gemini")
                matching_response = get_gemini_repsonse(prompt, temperature=0)

                # Initialize an empty dictionary to store the results
                result = {}

                # Split the text into lines
                lines = matching_response.strip().split('\n')
                
                # Process each line
                for line in lines:
                    # Extract JD Match Score
                    if line.startswith("JD Match Score:"):
                        try:
                            match = re.search(r'JD Match Score: (\d+)', line)
                            if match:
                                result["JD Match Score"] = int(match.group(1))
                        except ValueError:
                            print("JD Match Score is not a valid integer.")
                    
                    # Extract Profile Summary
                    elif line.startswith("Profile Summary:"):
                        result["Profile Summary"] = line.replace("Profile Summary:", "").strip()
                    
                    # Extract Missing Skills
                    elif line.startswith("Missing Skills:"):
                        result["Missing Skills"] = line.replace("Missing Skills:", "").strip()
                
                # Extract each component of the result dict
                matching_score = result["JD Match Score"]
                missingkeywords = result["Missing Skills"]
                profile_summary = result["Profile Summary"]
                logging.info("Gemini responsed and score extracted successfully")
                logging.info("-"*10)
                # Check matching score and update report
                generate_report(report_file, "Checking Matching Score")
                generate_report(report_file, f'Matching score: {matching_score}')
                generate_report(report_file, f'Missing Skills: {missingkeywords}')
                generate_report(report_file, f'Profile Summary: {profile_summary}')

                # Store these variables in session
                st.session_state['jd_text'] = preprocessed_jd_text
                st.session_state['cv_text'] = preprocessed_cv_text
                st.session_state['JD_Match_Score'] = matching_score
                st.session_state['Missing_Skills'] = missingkeywords
                st.session_state['Profile_Summary'] = profile_summary
                
                logging.info("Comparing threshold and navigate to cv_screening_feedback.py")
                # Logic 2: If CV not achieve the minimum score, reject the candidate
                if matching_score < cv_matching_threshold:
                    generate_report(report_file, "This candidate is not eligible because of low mathcing score")              
                    generate_report(report_file, "-"*10)
                    st.switch_page("pages/cv_screening_feedback.py")
                else:
                    generate_report(report_file, "This candidate is eligible because of high mathcing score")              
                    generate_report(report_file, "-"*10)
                    generate_report(report_file, "Moving to second round")
                    st.switch_page("pages/cv_screening_feedback.py")

                
except Exception as e:
    # Log the exception
    logging.error(f"An error occurred: {str(e)}")
    print(f"An error occurred: {str(e)}")
                