from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq


class llm_model:
    def __init__(self):
        self.gemini_llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")
        self.groq_llm = ChatGroq(model="deepseek-r1-distill-llama-70b")

    def gemini_llm_model(self):
        return self.gemini_llm

    def groq_llm_model(self):
        return self.groq_llm
