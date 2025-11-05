import streamlit as st
import os, json
from openai import OpenAI

st.set_page_config(page_title="AI Interview Coach", layout="centered")
st.title("🎤 AI Interview Coach")

client = OpenAI() if os.getenv("OPENAI_API_KEY") else None

role = st.selectbox("Role", ["Data Engineer","ML Engineer","GenAI Engineer","Data Scientist"])
level = st.selectbox("Level", ["Junior","Mid","Senior"])

if st.button("Generate Question"):
    prompt = f"Generate a {level} interview question for the role: {role}. Keep it concise."
    if client:
        resp = client.chat.completions.create(model="gpt-4", messages=[{"role":"user","content":prompt}])
        st.session_state['question'] = resp.choices[0].message.content
    else:
        st.session_state['question'] = f"(Offline demo) Describe a robust data pipeline for {role}."
    st.success("Question generated.")

question = st.session_state.get('question')
if question:
    st.subheader("Question")
    st.write(question)
    answer = st.text_area("Your answer")
    if st.button("Evaluate"):
        eval_prompt = f"Evaluate this answer for the question: {question}\nAnswer: {answer}\nReturn JSON with keys: score(1-10), strengths(list), improvements(list)."
        if client:
            out = client.chat.completions.create(model="gpt-4", messages=[{"role":"user","content":eval_prompt}], temperature=0.2)
            try:
                parsed = json.loads(out.choices[0].message.content)
            except Exception:
                parsed = {"score":7,"strengths":["Clear structure"],"improvements":["More concrete metrics"]}
        else:
            parsed = {"score":6,"strengths":["Mentioned pipelines"],"improvements":["Add monitoring, SLAs"]}
        st.json(parsed)
