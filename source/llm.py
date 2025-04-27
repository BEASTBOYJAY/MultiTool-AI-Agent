from langchain_google_genai import ChatGoogleGenerativeAI


class llm_model:
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")

    def run(self, query: str):
        result = self.llm.invoke(query)
        return result.content

    def model(self):
        return self.llm
