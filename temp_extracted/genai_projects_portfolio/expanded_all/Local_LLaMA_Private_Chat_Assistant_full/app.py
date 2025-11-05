import streamlit as st
import ollama, chromadb

st.set_page_config(page_title="Local LLaMA Assistant", layout="centered")
st.title("🦙 Local LLaMA Private Chat")

model = st.text_input("Model name", value="llama3")
client = chromadb.Client()
collection = client.create_collection("notes")

user_q = st.text_input("Ask anything:")
if st.button("Send") and user_q.strip():
    # naive: store question to local vector store for future retrieval demo
    collection.add(ids=[str(collection.count()+1)], documents=[user_q])
    try:
        resp = ollama.chat(model=model, messages=[{"role":"user","content":user_q}])
        st.write(resp['message']['content'])
    except Exception as e:
        st.error("Ollama not available. Start Ollama and pull a model first.")
