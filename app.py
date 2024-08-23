from dotenv import load_dotenv

load_dotenv()

import base64
import streamlit as st
# from streamlit.components.v1 import html
import os
import io
from PIL import Image
import pdf2image
import google.generativeai as genai


genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(option,input,pdf_content,prompt):
    model=genai.GenerativeModel('gemini-1.5-flash')
    response=model.generate_content([option,input,pdf_content[0],prompt])
    # print("Reponse Text:", response.text)
    return response.text

def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:

        images=pdf2image.convert_from_bytes(uploaded_file.read())

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
        # print('img_byte_arr:',img_byte_arr)
        return pdf_parts
    else:
        raise FileNotFoundError("No file uploaded")

## StreamLit App
st.set_page_config(page_title="ATS Tracking System")
st.header("ATS Tracking System")
# option = st.selectbox(
#     'Select the Job profile ou are applying for...',
#     ("Data Science", "Full Stack Web Development", "Big Data Engineering", "DEVOPS", "Data Analyst", "Data Visualisation"), 
#     index=None,
#     placeholder="Select Job profile..."
#      )
option = st.text_input("Job Profile:", key="profile")
st.write('You are applying for', option, 'role')
input_text=st.text_area("Job Descriptiion: ", key="input")
uploaded_file=st.file_uploader("Upload your Resume (in PDF)", type=["pdf"])

if uploaded_file is not None:
    st.write("PDF Uploaded Sucessfully")

submit1 = st.button("Tell me about the Resume")

submit2 = st.button("Percentage Match")

input_prompt1= """
You are an experienced HR with Tech Expirence in the field of {option}, your task is to review the provided {uploaded_file} against the {input_text} for {option} profiles only.
If you get any other {input_text} that doesn'tmacthes the {option},please tell that the Job profile and Job Description doesn't matches, that's it.
If you get any other {uploaded_file} that doesn't macthes the {option},please tell that the Resume is not for {option}, that's it.
If you get any other {input_text} that aligns with {option},only and only then do the following
Please share your professional evaluation on whether the candidate's profile aligns with the role.
Higlight the strengths and weaknesses of the application in realtion to the specific job requirmnets.
"""
input_prompt2= """
You are an skilled ATS (Application Tracking System) scanner with a deep understanding of any one job role {option} and deep ATS functionality,
your task is to review the provided resume against the {input_text} for {option} profile only.First line should Give the percentage match bewtween the {input_text} and {uploaded_file}, then 
please check the following, 
If you get any other {input_text} doesn'tmacthes the {option},please tell that the Job profile and Job Description doesn't matches, that's it.
If you get any other {uploaded_file} doesn't macthes the {option},please tell that the resume is not for {option}, that's it.
If you get any other {input_text} that aligns with {option} only and only then do the following,

If the resume matches the job description, then provide the list keyword missing which can help to clear the ATS,then
Strength of the resume based on their skills in percentage.
Then List the skills and how much relavant they are with Job description,
then point out the specifics words/lines/section/placing from the resume to change (if any), then
top 5 things that candidate should add in his/her resume to get hired, then
5 job description domain related projects to add to resume that might make candidate stand out 
and last the final thoughts.

At the end if the candidate's {uploaded_file} is fit to apply for the {input_text} or not and 
whether the candidate should apply for the {input_text}, and don't be diplomatic.

Also don't give generic  results, the result should be strictly in correlation with the {input_text} and {uploaded_file}
"""

if submit1 :
    if uploaded_file is not None:
        pdf_content=input_pdf_setup(uploaded_file)
        response=get_gemini_response(option,input_prompt1,pdf_content,input_text)
        st.subheader("The Response is:")
        st.write(response)
    else:
        st.write("Please upload the Resume")
elif submit2 :
    if uploaded_file is not None:
        pdf_content=input_pdf_setup(uploaded_file)
        response=get_gemini_response(option,input_prompt2,pdf_content,input_text)
        st.subheader("The Response is:")
        st.write(response)
    else:
        st.write("Please upload the Resume")



# input_prompt1= """
# You are an experienced HR with Tech Expirence in the field of any one job role from Data Science, Full Stack Web Development, Big Data
# Engineering, DEVOPS, Data Analyst, Data Visualisation, your task is to review the provided resume against the job
# description for these profiles.
# Please share your professional evaluation on whether the candidate's profile aligns with the role.
# Higlight the strengths and weaknesses of the application in realtion to the specific job requirmnets.
# """
# input_prompt2= """
# You are an skilled ATS (Application Tracking System) scanner with a deep understanding of any one job role Data Science, Full 
# Stack Web Development, Big Data Engineering, DEVOPS, Data Analyst, Data Visualisation and deep ATS functionality,
# your task is to review the provided resume against the job description for these profiles. Give the percentage match
# if the resume matches the job description. 
# First outcome should come as percentage and then the keyword missing,
# Strength of the resume based in their skills in percentage. List the skills and how much relavant they are with JD,
# Also point out the specifics words/lines/section/placing from the resume to change (if any),
# top 5 things that candidate should add in his/her resume to get hired, 
# 5 job description domain related projects to add to resume that might make candidate stand out 
# and last the final thoughts. 
# """
