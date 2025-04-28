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

        template = """Answer the following questions as best you can. 
        You have access to the following tools:

        {tools}

        Previous conversation history:
        {chat_history}

        Use the following format exactly:

        Question: the input question you must answer
        Thought: you should always think about what to do
        (If you know the answer) Final Answer: your direct final answer (must begin with 'Final Answer:')
        (If you need to use a tool) Action: the action to take, should be one of [{tool_names}]
        Action Input: the input to the action
        Observation: the result of the action
        Thought: think what to do next
        Final Answer: your final answer to the original question

        Important rules:
        - After every 'Thought:', you must either output 'Action:' or 'Final Answer:' immediately.
        - Do not write responses without labeling them as 'Final Answer:'.
        - Stay strictly inside the required format, otherwise the system will raise an error.

        Begin!

        Question: {input}
        Thought:{agent_scratchpad}
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
    agent = Agent(model_type="groq")
    agent.run()
