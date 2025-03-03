import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
import logging
import re
from cv_screening import generate_report, get_gemini_repsonse

load_dotenv()  # Load environment variables
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
# Hide the sidebar
st.sidebar.empty()

# Accessing stored data
if 'jd_text' in st.session_state:
    jd_text = st.session_state['jd_text']
if 'cv_text' in st.session_state:
    cv_text = st.session_state['cv_text']

# Report fie
report_file = r'report.txt'

# Display Header in streamlit
st.header("Interviewing with an AI Agent Round")
st.subheader("Please answer the following questions")

# Update report
generate_report(report_file, "Interviewing with an AI Agent Round")
generate_report(report_file, "-"*10)

prompt = f"""
        Job Description: {jd_text}
        Candidate Profile: {cv_text}

        Based on the above job description and candidate profile, generate:
        1. One technical questions.
        2. One behavioral questions.
        3. One experience-related questions.

        Generate three interview questions in this format:
        
        Technical Questions: 
        Behavioral Questions: 
        Experience-based Question: 
        """
# Run the prompt
interview_questions = get_gemini_repsonse(prompt, temperature=0)


lines = [item for item in interview_questions.strip().split('\n') if item.strip()]


tech_question = lines[1] if len(lines) > 1 else "No technical question found"
behav_question = lines[3] if len(lines) > 3 else "No behavioral question found"
experienced_question = lines[5] if len(lines) > 5 else "No experienced-based question found"


# Display questions and allow answers of max 500 characters
st.markdown(f'Technical Question: {tech_question}')
tech_answer = st.text_area("Answer for the Technical question", max_chars=500, height=200)

st.markdown(f'Behavioral Question: {behav_question}')
behav_answer = st.text_area("Answer for the Behavioral question", max_chars=500, height=200)

st.markdown(f'Experienced Question: {experienced_question}')
experience_answer = st.text_area("Answer for the Experienced-related question", max_chars=500, height=200)

def parse_response(text):
    # Initialize an empty dictionary to store the results
    result = {}
    
    overall_score = re.search(r"Overall Score:\s*(.*)", text)
    if overall_score:
        result["Overall Score"] = overall_score.group(1).strip("").strip("**")
    
    return result


# Submit technical answer
check_answer = st.button("Submit Answer", key="submit_answer")
if check_answer:
    # Use Gemini to evaluate Technical response
    prompt_tech_evaluate = f"""
                                Question: {tech_question}
                                Candidate response: {tech_answer}
                                Evaluate candidate responses for relevance, correctness, and completeness.
                                I want the response have a structure of 5 lines. 
                                Relevance: feedback. Relevance Score: (scale 0-100)
                                Correctness: feedback. Correctness Score: (scale 0-100)
                                Completeness: feedback. Completeness Score:(scale 0-100)
                                Overall Score: (average of Relevance Score, Correctness Score and Completeness Score)
                                Overall Feedback: (max 50 words)
                                """
    tech_answer_evaluation = get_gemini_repsonse(prompt_tech_evaluate, temperature=0)
    tech_answer_evaluation_dict = parse_response(tech_answer_evaluation)
    # Extract the overall score for this answer
    tech_answer_overall_score = float(tech_answer_evaluation_dict['Overall Score'])
    # Update report
    generate_report(report_file, "Technical Question")
    generate_report(report_file, "-"*10)
    generate_report(report_file, f"{tech_question}")
    generate_report(report_file, "-"*10)
    generate_report(report_file, f"{tech_answer}")
    generate_report(report_file, "-"*10)
    generate_report(report_file, f"{tech_answer_evaluation}")

    # Use Gemini to evaluate Behavioral response
    prompt_behav_evaluate = f"""
                                Question: {behav_question}
                                Candidate response: {behav_answer}
                                Evaluate candidate responses for relevance, correctness, and completeness.
                                I want the response have a structure of 5 lines. 
                                Relevance: feedback. Relevance Score: (scale 0-100)
                                Correctness: feedback. Correctness Score: (scale 0-100)
                                Completeness: feedback. Completeness Score:(scale 0-100)
                                Overall Score: (average of Relevance Score, Correctness Score and Completeness Score)
                                Overall Feedback: (max 50 words)
                                """
    behav_answer_evaluation = get_gemini_repsonse(prompt_behav_evaluate, temperature=0)
    behav_answer_evaluation_dict = parse_response(behav_answer_evaluation)
    # Extract the overall score for this answer
    behav_answer_overall_score = float(behav_answer_evaluation_dict['Overall Score'])
    # Update report
    generate_report(report_file, "Behavioral Question")
    generate_report(report_file, "-"*10)
    generate_report(report_file, f"{behav_question}")
    generate_report(report_file, "-"*10)
    generate_report(report_file, f"{behav_answer}")
    generate_report(report_file, "-"*10)
    generate_report(report_file, f"{behav_answer_evaluation}")

    # Use Gemini to evaluate Experienced-related response
    prompt_exp_evaluate = f"""
                                Question: {experienced_question}
                                Candidate response: {experience_answer}
                                Evaluate candidate responses for relevance, correctness, and completeness.
                                I want the response have a structure of 5 lines. 
                                Relevance: feedback. Relevance Score: (scale 0-100)
                                Correctness: feedback. Correctness Score: (scale 0-100)
                                Completeness: feedback. Completeness Score:(scale 0-100)
                                Overall Score: (average of Relevance Score, Correctness Score and Completeness Score)
                                Overall Feedback: (max 50 words)
                                """
    exp_answer_evaluation = get_gemini_repsonse(prompt_exp_evaluate, temperature=0)
    exp_answer_evaluation_dict = parse_response(exp_answer_evaluation)
    
    # Extract the overall score for this answer
    exp_answer_overall_score = float(exp_answer_evaluation_dict['Overall Score'])
    # Update report
    generate_report(report_file, "Experienced-related Question")
    generate_report(report_file, "-"*10)
    generate_report(report_file, f"{experienced_question}")
    generate_report(report_file, "-"*10)
    generate_report(report_file, f"{experience_answer}")
    generate_report(report_file, "-"*10)
    generate_report(report_file, f"{exp_answer_evaluation}")

    # Display feedback from Gemini
    st.markdown(f'Feedback for the answer of technical question: {tech_answer_evaluation}')
    st.markdown(f'Feedback for the answer of behavioral question: {behav_answer_evaluation}')
    st.markdown(f'Feedback for the answer of experienced-related question: {exp_answer_evaluation}')
    
    # Candidate overall score
    candidate_overall_score = (tech_answer_overall_score + behav_answer_overall_score + exp_answer_overall_score)/3
    
    # Remember technical part
    st.session_state['tech_question'] = tech_question
    st.session_state['tech_answer'] = tech_answer
    st.session_state['tech_answer_evaluation'] = tech_answer_evaluation
    # Remember behavioral part
    st.session_state['behav_question'] = behav_question
    st.session_state['behav_answer'] = behav_answer
    st.session_state['behav_answer_evaluation'] = behav_answer_evaluation
    # Remember experienced-relationed part
    st.session_state['experienced_question'] = experienced_question
    st.session_state['experience_answer'] = experience_answer
    st.session_state['exp_answer_evaluation'] = exp_answer_evaluation
    # Remember candidate overall score
    st.session_state['candidate_overall_score'] = candidate_overall_score
    # Move to nterview_feedback.py page
    st.switch_page("pages/interview_feedback.py")



