from openai import OpenAI
import streamlit as st
from fpdf import FPDF

st.set_page_config(page_title="AI Resume Builder", page_icon="🤖")

st.title("🤖 AI Resume Builder")
st.write("Generate a professional resume using OpenAI GPT.")

with st.sidebar:
    api_key = st.text_input("Enter your OpenAI API Key", type="password")
    st.info("Get your API key from https://platform.openai.com/account/api-keys")

name = st.text_input("Full Name")
email = st.text_input("Email")
phone = st.text_input("Phone")
summary = st.text_area("Professional Summary")
skills = st.text_area("Skills (comma separated)")
experience = st.text_area("Work Experience (one per line)")
education = st.text_area("Education (one per line)")

def generate_resume(prompt_text):
    client = OpenAI(api_key=api_key)
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a professional resume writer."},
            {"role": "user", "content": prompt_text}
        ]
    )
    return completion.choices[0].message.content

def create_pdf(resume_text):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    for line in resume_text.split("\n"):
        pdf.multi_cell(0, 10, line)
    pdf.output("resume.pdf")

if st.button("🚀 Generate Resume"):
    if not api_key:
        st.error("Please provide your OpenAI API key.")
    else:
        prompt = f"""
        Create a professional resume for:
        Name: {name}
        Email: {email}
        Phone: {phone}
        Summary: {summary}
        Skills: {skills}
        Experience: {experience}
        Education: {education}
        Format it neatly with sections.
        """
        with st.spinner("Generating resume..."):
            resume_text = generate_resume(prompt)
            create_pdf(resume_text)
            st.success("✅ Resume generated successfully!")
            with open("resume.pdf", "rb") as pdf_file:
                st.download_button("⬇️ Download Resume PDF", pdf_file, file_name="AI_Resume.pdf")

st.caption("Created by Sumedha Bhosale | Powered by OpenAI GPT-3.5")
