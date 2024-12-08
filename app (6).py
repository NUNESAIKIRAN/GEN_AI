import streamlit as st
import pdfplumber as pdf
import google.generativeai as ai

st.title("PDF Extraction and Question Answering")


with st.sidebar:
    st.title("upload the pdf's")
    upload_pdf = st.file_uploader(label = "Choose a PDF file",type='pdf')
    if upload_pdf:
        st.button("submit")

#-------------------------------------------------------------------------------------------------------

KEY = "AIzaSyAXpYE3MbV28HHzRGhCh827hgZOIUKVLnA"
ai.configure(api_key=KEY)

#-------------------------------------------------------------------------------------------------------

def pdf_extraction(pdf_path):
    with pdf.open(pdf_path) as pdf_file:
        text = ""
        for page in pdf_file.pages:
            text = text + page.extract_text()
    return text

#--------------------------------------------------------------------------------------------------------

def ask_question(content, question):
    model = ai.GenerativeModel(model_name="models/gemini-1.5-flash")
    prompt=f"{content}\n\nQuestion: {question}\nAnswer:"
    responce = model.generate_content(prompt)
    if responce:
        return responce.text
    else:
        return "No answer generated."

#---------------------------------------------------------------------------------------------------------


if upload_pdf:
    # Extract text from uploaded PDF
    content = pdf_extraction(upload_pdf)
    # Input for user question
    user_question = st.text_input("Ask a Question About the PDF Content:")
    if st.button("Submit"):
        # Generate answer
        answer = ask_question(content, user_question)
        st.write("Answer:", answer)
        