import streamlit as st
from fpdf import FPDF
from dotenv import load_dotenv
import os
import google.generativeai as genai

# Load environment variables
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

# Configure Gemini API
genai.configure(api_key=api_key)

# Streamlit UI
st.set_page_config(page_title="AI Resume Builder (Gemini)", page_icon="🪄")

st.title("🪄 AI Resume Builder (Gemini)")
st.write("Generate a professional resume using **Google Gemini 1.5 Pro**.")

# Sidebar for key input
with st.sidebar:
    api_key_input = st.text_input("Enter your Gemini API Key", type="password")
    if api_key_input:
        genai.configure(api_key=api_key_input)
    st.info("Get your API key from [Google AI Studio](https://aistudio.google.com/app/apikey)")

# Form Inputs
name = st.text_input("Full Name")
email = st.text_input("Email")
phone = st.text_input("Phone")
summary = st.text_area("Professional Summary")
skills = st.text_area("Skills (comma separated)")
experience = st.text_area("Work Experience (one per line)")
education = st.text_area("Education (one per line)")

# --- Gemini Resume Generation Function ---
def generate_resume(prompt_text):
    model = genai.GenerativeModel("gemini-2.5-flash")
    response = model.generate_content(prompt_text)
    return response.text

# --- PDF Creator ---
def create_pdf(resume_text):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    for line in resume_text.split("\n"):
        pdf.multi_cell(0, 10, line)
    pdf.output("resume.pdf")

# --- Main Logic ---
if st.button("🚀 Generate Resume"):
    if not api_key and not api_key_input:
        st.error("Please provide your Gemini API key.")
    else:
        prompt = f"""
        You are a professional resume writer.
        Create a resume for:
        Name: {name}
        Email: {email}
        Phone: {phone}
        Summary: {summary}
        Skills: {skills}
        Experience: {experience}
        Education: {education}
        Format it neatly with sections and bullet points.
        """
        with st.spinner("✨ Gemini is generating your resume..."):
            try:
                resume_text = generate_resume(prompt)
                create_pdf(resume_text)
                st.success("✅ Resume generated successfully!")
                with open("resume.pdf", "rb") as pdf_file:
                    st.download_button("⬇️ Download Resume PDF", pdf_file, file_name="AI_Resume_Gemini.pdf")
            except Exception as e:
                st.error(f"❌ Error: {e}")

st.caption("Created by Sumedha Bhosale | Powered by Google Gemini 1.5 Pro 🌸")
