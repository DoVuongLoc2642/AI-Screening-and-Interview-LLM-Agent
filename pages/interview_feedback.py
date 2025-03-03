import streamlit as st

# Hide the sidebar
st.sidebar.empty()

# Display streamlit title
st.title("Interview Feedback")

# Define overall_score threshold
overall_score_threshold = 70

# Accessing stored data
if 'jd_text' in st.session_state:
    jd_text = st.session_state['jd_text']
if 'cv_text' in st.session_state:
    cv_text = st.session_state['cv_text']
if 'tech_question' in st.session_state:
    tech_question = st.session_state['tech_question']
    st.write("Technical Question")
    st.write(tech_question)
if 'tech_answer' in st.session_state:
    tech_answer = st.session_state['tech_answer']
    st.write("Technical Answer")
    st.write(tech_answer) 
if 'tech_answer_evaluation' in st.session_state:
    tech_answer_evaluation = st.session_state['tech_answer_evaluation'] 
    st.write("Technical Feedback")
    st.write(tech_answer_evaluation) 
    st.write("-"*10)
if 'behav_question' in st.session_state:
    behav_question = st.session_state['behav_question'] 
    st.write("Behvioral Question")
    st.write(behav_question) 
if 'behav_answer' in st.session_state:        
    behav_answer = st.session_state['behav_answer']
    st.write("Behvioral Answer")
    st.write(behav_answer) 
if 'behav_answer_evaluation' in st.session_state:
    behav_answer_evaluation = st.session_state['behav_answer_evaluation'] 
    st.write("Behvioral Feedback")
    st.write(behav_answer_evaluation) 
    st.write("-"*10)
if 'experienced_question' in st.session_state:
    experienced_question = st.session_state['experienced_question']
    st.write("Experienced-related Question")
    st.write(experienced_question)
if 'experience_answer' in st.session_state:
    experience_answer = st.session_state['experience_answer'] 
    st.write("Experienced-related Answer")
    st.write(experience_answer)
if 'exp_answer_evaluation' in st.session_state:
    exp_answer_evaluation = st.session_state['exp_answer_evaluation']  
    st.write("Experienced-related Feedback")
    st.write(exp_answer_evaluation)
    st.write("-"*10)
if 'candidate_overall_score' in st.session_state:
    candidate_overall_score = st.session_state['candidate_overall_score'] 
    st.write("Overall Score")
    st.write(candidate_overall_score)

    if candidate_overall_score < overall_score_threshold:
        st.write(f"Unfortunately, you did not pass the interview. The minimum score is {overall_score_threshold}")
    else:
        st.subheader(f"Congratulaions, you passed the test.")
        st.write("Please click the button below to move to the last round")
        next_round_button = st.button("Move to final round")
        if next_round_button:
            st.switch_page("pages/QA.py")
