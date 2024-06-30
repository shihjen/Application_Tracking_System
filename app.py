import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
import PyPDF2

st.set_page_config(page_title = 'GeminiAI TalentScout',
                   page_icon = '',
                   layout = 'wide',
                   initial_sidebar_state = 'auto')

load_dotenv()
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

# function to get Gemini-Pro response
def gemini_response(input):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(input)
    return response.text

# function to convert/extract info from pdf to text
def extract_text(uploaded_file):
    reader = PyPDF2.PdfReader(uploaded_file)
    text = ""
    for page in range (len(reader.pages)):
        page = reader.pages[page]
        page_content = str(page.extract_text())
        text += page_content
    return text

# write a prompt template
prompt = '''
Please act Like a skilled or very experience Application Tracking System (ATS) with a deep understanding of tech field, software engineering, data science, data analyst, and data engineer. 
Your task is to evaluate the resume based on the given job description.
You must consider the job market is very competitive and you should provide best assistance for improving the resumes. 
Assign the percentage Matching based on job description and the missing keywords with high accuracy. resume:{text} description:{job_description}

I want the response in the bulletin point, containes only the following 2 elements.
- Job Description Match (%):
- Missing Keywords:
- Summary of the Resume: 
'''

col1, col2 = st.columns([1.5,2], gap='medium')

with col1:
    st.title('GeminiAI TalentScout')
    job_description = st.text_area('Paste the Job Description', height=400)
    uploaded_file = st.file_uploader('Upload Resume', type=['pdf'], accept_multiple_files=False)
    submit = st.button('Submit')

with col2:
    st.header('Candidate Fit Assessment', divider='gray')
    if submit:
        if uploaded_file is not None:
            text = extract_text(uploaded_file)
            analysis = gemini_response(prompt)
            st.markdown(f'#### {analysis}')