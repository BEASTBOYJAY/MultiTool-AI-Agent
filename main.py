from source.llm import llm_model
from source.tools import Tools
from langchain.agents import AgentExecutor, create_react_agent
from langchain_core.prompts import PromptTemplate


class Agent:
    def __init__(self):
        self.llm = llm_model().model()
        self.tools = Tools().run()
        template = """Answer the following questions as best you can. You have access to the following tools:

        {tools}

        Use the following format:

        Question: the input question you must answer
        Thought: you should always think about what to do
        (If you know the answer) Final Answer: [your answer directly]
        (If you need to use a tool) Action: the action to take, should be one of [{tool_names}]
        Action Input: the input to the action
        Observation: the result of the action
        Thought: I now know the final answer
        Final Answer: the final answer to the original input question

        Begin!

        Question: {input}
        Thought:{agent_scratchpad}"""

        self.prompt = PromptTemplate.from_template(template)

    def run(self):
        agent = create_react_agent(llm=self.llm, tools=self.tools, prompt=self.prompt)

        agent_executor = AgentExecutor(
            agent=agent,
            tools=self.tools,
            verbose=True,
            max_iterations=3,
            handle_parsing_errors=True,
        )

        while True:
            user_input = input("\nAsk your AI agent: ")
            if user_input.lower() in ["exit", "quit", "bye"]:
                print("Goodbye! 👋")
                break
            try:
                result = agent_executor.invoke({"input": user_input})
                print(f"\nAgent Response:\n{result["output"]}")
            except Exception as e:
                print(f"\n⚠️ An error occurred: {e}")


if __name__ == "__main__":
    agent = Agent()
    agent.run()
