from dotenv import load_dotenv

load_dotenv()
import base64
import streamlit as st
import os
import io
from PIL import Image
import pdf2image
import google.generativeai as genai
import sqlite3

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


def get_gemini_response(input,pdf_content,prompt):
    model=genai.GenerativeModel('gemini-pro-vision')
    response=model.generate_content([input,pdf_content[0],prompt])
    return response.text

def store_data(input_text, pdf_content):
    conn = sqlite3.connect('S:\Project\ATS Tracker\resume_database.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS resumes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            input_text TEXT,
            pdf_content TEXT
        )
    ''')

    cursor.execute('''
        INSERT INTO resumes (input_text, pdf_content)
        VALUES (?, ?)
    ''', (input_text, pdf_content))

    conn.commit()
    conn.close()

def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        poppler_path="./venv/Library/Library/bin" 
        images=pdf2image.convert_from_bytes(uploaded_file.read(), poppler_path=poppler_path)

        first_page=images[0]

        img_byte_arr = io.BytesIO()
        first_page.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()

        pdf_parts = [
            {
                "mime_type": "image/jpeg",
                "data": base64.b64encode(img_byte_arr).decode()
            }
        ]
        return pdf_parts
    else:
        raise FileNotFoundError("No file uploaded")
    
## StreamLit App
    
st.set_page_config(page_title='ATS Resume Evaluator')
st.header("ATS Tracking System")
input_text=st.text_area("Job Descriptiion: ", key="input")
uploaded_file=st.file_uploader("Upload your Resume (in PDF)", type=["pdf"])

if uploaded_file is not None:
    st.write("PDF Uploaded Sucessfully")

submit1 = st.button("Tell me about the Resume")

submit2 = st.button("Percentage Match")

input_prompt1= """
You are an experienced HR with Tech Expirence in the field of any one job role from Data Science, Full Stack Web Development, Big Data
Engineering, DEVOPS, Data Analyst, Data Visualisation, your task is to review the provided resume against the job
description for these profiles.
Please share your professional evaluation on whether the candidate's profile aligns with the role.
Higlight the strengths and weaknesses of the application in realtion to the specific job requirmnets.
"""
input_prompt2= """
You are an skilled ATS (Application Tracking System) scanner with a deep understanding of any one job role Data Science, Full 
Stack Web Development, Big Data Engineering, DEVOPS, Data Analyst, Data Visualisation and deep ATS functionality,
your task is to review the provided resume against the job description for these profiles. Give the percentage match
if the resume matches the job description. 
First outcome should come as percentage and then the keyword missing,
Strength of the resume based in their skills in percentage. List the skills and how much relavant they are with JD,
Also point out the specifics words/lines/section/placing from the resume to change (if any),
top 5 things that candidate should add in his/her resume to get hired, 
5 job description domain related projects to add to resume that might make candidate stand out 
and last the final thoughts. 
"""


if submit1:
    if uploaded_file is not None:
        pdf_content=input_pdf_setup(uploaded_file)
        response=get_gemini_response(input_prompt1,pdf_content,input_text)
        st.subheader("The Response is:")
        st.write(response)
    else:
        st.write("Please upload the Resume")
elif submit2:
    if uploaded_file is not None:
        pdf_content=input_pdf_setup(uploaded_file)
        response=get_gemini_response(input_prompt2,pdf_content,input_text)
        st.subheader("The Response is:")
        st.write(response)
    else:
        st.write("Please upload the Resume")

