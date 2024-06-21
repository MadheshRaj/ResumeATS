import streamlit as st
import google.generativeai as genai
import os
from PyPDF2 import PdfReader
from dotenv import load_dotenv
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_response(input,pdf_text,prompt):
    model = genai.GenerativeModel("gemini-pro")
    response=model.generate_content([input,pdf_text,prompt])
    return response.text

def get_pdf_text(uploaded_file):
    text=""
    reader=PdfReader(uploaded_file)
    for page in reader.pages:
        text+=page.extract_text()
    return text

st.set_page_config(page_title="ATS Resume")
st.title("Resume Applicant Tracking System")
jr=st.selectbox("Choose your role",["Job Seekers","Job Recruiters"])
jd=st.text_area("Enter detailed Job description",key="input")
file=st.file_uploader("Upload the resume(PDF)....", type=["PDF"])

if file is not None:
    st.write("PDF Uploaded Successfully")

submit=st.button("Submit")

if submit:
    if file is not None:
        text=get_pdf_text(file)
        if jr == "Job Seekers":
            prompt=""" You are an experienced Human Resource Manager with technical experience in the field of any one 
                       job role from Data Science,Full Stack Web Development, Big data Engineering, DEVOPS,Data Analyst,
                       your task is to review the provided resume based on the job description. 
                       Please share your professional evaluation on whether the candidate's profile aligns with the role. 
                       Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements.
                       Assign the missing keywords with high accuracy.You must consider the job market is very competitive and you should provide 
                       best assistance for improving thr resumes."""
            st.subheader("The Response is:")
            response=get_response(jd,text,prompt)
            st.write(response)
        elif jr=="Job Recruiters":
            prompt=""" You are an skilled ATS (Applicant Tracking System) scanner with a deep understanding of any one job role data science,
                       Full Stack Web Development,Big data Engineering,DEVOPS,Data Analyst and deep ATS functionality, 
                       your task is to evaluate the resume against the provided job description. give me the percentage of match if the resume matches
                       the job description. The output should be only in number without percentage symbol"""
            response=get_response(jd,text,prompt)
            percentage=int(response)
            st.subheader("The Response is:")
            st.slider("Percentage Match:",0,100,percentage)
    else:
        st.write("Please upload the resume")