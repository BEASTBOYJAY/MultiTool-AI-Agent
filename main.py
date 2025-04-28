from source.llm import llm_model
from source.tools import Tools
from langchain.agents import AgentExecutor, create_react_agent
from langchain_core.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory


class Agent:
    def __init__(self, model_type: str):
        if model_type == "gemini":
            self.llm = llm_model().gemini_llm_model()
        else:
            self.llm = llm_model().groq_llm_model()

        self.tools = Tools().run()
        self.memory = ConversationBufferMemory(
            memory_key="chat_history", return_messages=True
        )

        template = """You are an intelligent, thoughtful AI assistant. 
        You can reason carefully, use tools when needed, and communicate clearly.

        Your abilities:
        - You can use the following tools when needed:
        {tools}

        - You remember the conversation so far:
        {chat_history}

        When answering, follow this format:
        ---
        Question: [The question or instruction from the user]

        Thought: [Think carefully about what is being asked. Plan step-by-step what you should do.]

        (If you need to use a tool)
        Action: [Select one tool to use, exactly as named in [{tool_names}]]
        Action Input: [Provide the input for the tool]

        (After observing the tool's output)
        Observation: [Record what you saw]

        Thought: [Reflect on the observation. Decide if you can now answer, or need another action.]

        Final Answer: [Give a clear, helpful answer to the user.]
        ---

        General rules:
        - Be concise but thoughtful.
        - Use tools only if necessary.
        - If unsure, explain your reasoning honestly.
        - Always aim to be accurate and helpful.

        Now begin!

        Question: {input}
        {agent_scratchpad}
        """

        self.prompt = PromptTemplate.from_template(template)

    def run(self):
        agent = create_react_agent(llm=self.llm, tools=self.tools, prompt=self.prompt)

        agent_executor = AgentExecutor(
            agent=agent,
            tools=self.tools,
            verbose=True,
            # max_iterations=6,
            handle_parsing_errors=True,
            memory=self.memory,
            # early_stopping_method="generate",
        )

        while True:
            user_input = input("\nAsk your AI agent: ")
            if user_input.lower() in ["exit", "quit", "bye"]:
                print("Goodbye! 👋")
                break
            try:
                result = agent_executor.invoke({"input": user_input})
                print(f"\nAgent Response:\n{result['output']}")
            except Exception as e:
                print(f"\n⚠️ An error occurred: {e}")


if __name__ == "__main__":
    agent = Agent(model_type="gemini")
    agent.run()
