# AI-Screening-and-Interview-LLM-Agent

Interview processes are often time-consuming and costly, with companies investing over $5,000 per hire, primarily due to the time spent by internal recruiters and hiring managers. On average, the interview process takes around 30 days to complete. To address this challenge, we introduce an LLM agent called SmartScreenAI: AI-Screening-and-Interview-Agent—an automated system designed to streamline candidate screening and conduting AI-driven interviews. The agent includes an advanced CV Screening feature to automate the candidate evaluation process before processing to the interview stage. Then, it customizes questions based on job requirements and candidate experience, evaluates responses, and generates an assessment report. The system focuses on screening and technical interviews in English, helping recruiters streamline hiring. 

## Technologies Used 

- **Streamlit**: For building the web interface.

- **Google Gemini AI**: For generating questions and evaluating responses.

- **PyPDF2**: For extracting text from PDF files.

- **NLTK**: For text preprocessing (tokenization, stopwords removal).

- **FPDF**: For generating PDF reports.

# Installation

Create a conda virtual environment and activate it:

```
conda create -n my_env python=3.10.0 -y
source activate my_env
```
Then, install the following packages in the requirements packages: ```pip install -r requirements.txt```  

# Usage

## Step 1: Generate an Google API key to use Gemini model 
Visit this link to generate your API key: https://aistudio.google.com/app/apikey

Once generated, store the API key in the .env file as follows: ```GOOGLE_API_KEY = 'place your API key here```

## Step 2: Set up the virtual environment
Create virtual environment and install the required libraries inside requirements.txt

## Step 3: Running the script
To operate the project, use the following command in the terminal:
```
 streamlit run cv_screening.py --server.enableXsrfProtection=false
```

# Input Requirements

- Job Description: A document detailing the company's background, job responsibilities, required skills, and preferred experience for the role.

- Candidate Profile: A document containing information about the candidate, such as their experience, skills, location, education, and other relevant details.

# Description

The Project will have these fundamental features:

- Dynamic Question Generation: The Agent should generate questions on-the-fly, tailored to the job description and candidate profile. This includes technical, behavioral, and experience-related questions, with the ability to ask follow-up questions based on the candidate’s responses.

- Response Evaluation: The Agent must assess candidate answers for relevance, accuracy, and completeness, providing feedback to the candidate accordingly.

- Contextual Guardrails: The Agent must have built-in safeguards to remain within the scope of the interview, avoiding responses to unrelated questions from candidates.

- Text-Based Interview Format: The interview should be conducted in a text-based (chat-style) format.

## Feature Details:

**1.	CV Screening**
   
- Upload CV and Job Description (JD) in PDF format.

- Check language compatibility between CV and JD.

- Evaluate CV against JD using AI to calculate a matching score.

- Provide feedback on missing skills and profile summary.

**2.	AI Interview**

- Generate technical, behavioral, and experience-related questions based on the CV and JD.

- Evaluate candidate responses using AI for relevance, correctness, and completeness.

- Calculate an overall score for the interview.

**3.	Final Q&A Round**
   
- Allow candidates to ask up to 3 work-related questions.

- Record questions and answers in the report.

**4.	Report Generation**
   
- Generate a detailed report in both .txt and .pdf formats.

- Include feedback, scores, and responses from each stage.


# Demo




