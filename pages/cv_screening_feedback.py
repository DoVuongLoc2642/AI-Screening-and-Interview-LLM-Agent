import streamlit as st

# Hide the sidebar
st.sidebar.empty()
st.title("CV Screening Feedback")
st.write("-"*10)

cv_matching_threshold = 50

# Accessing stored data
if 'cv_language' in st.session_state:
    cv_language = st.session_state['cv_language']
if 'jd_lang' in st.session_state:
    jd_lang = st.session_state['jd_lang']

if cv_language != jd_lang:
    st.text("You are not eligible due to CV not match the requried language")
else:
    st.text("Your language matched the Job Desciption")
    if 'JD_Match_Score' in st.session_state:
        JD_Match_Score = st.session_state['JD_Match_Score']
        st.text(f"In feedback: {JD_Match_Score}")
    else:
        st.text("Error here")

    if 'Missing_Skills' in st.session_state:
        Missing_Skills = st.session_state['Missing_Skills']
    if 'Profile_Summary' in st.session_state: 
        Profile_Summary = st.session_state['Profile_Summary'] 

    # Display feedback    
    st.write("------------ CV Feedback ------------")
    st.write(f"Matching score: {JD_Match_Score}")
    st.write(f"Missing skills: {Missing_Skills}")
    st.write(f"Profile Summary: {Profile_Summary}")

    if JD_Match_Score < cv_matching_threshold:
        st.text(f'Unfortunately, you did not match the requirements.')
    else:
        st.text(f'Congratulations, you have passed the CV Screening Round!!!')
        st.text(f'Please click the button below to move to second round!!!')
        second_round_button = st.button("Move to Second Round")
        if second_round_button:
            st.switch_page("pages/interview.py")