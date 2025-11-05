from fastapi import FastAPI
from pydantic import BaseModel
from langchain import PromptTemplate, OpenAI, LLMChain
import os

app = FastAPI(title="Email Assistant API")

template = "Thread summary: {thread}.\nWrite a concise professional reply addressing the key points. Tone: friendly and clear."
prompt = PromptTemplate.from_template(template)
llm = OpenAI(temperature=0.3)
chain = LLMChain(llm=llm, prompt=prompt)

class Inp(BaseModel):
    thread: str

@app.post("/reply")
def reply(inp: Inp):
    text = chain.run({"thread": inp.thread})
    return {"reply": text}
