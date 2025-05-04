# AI Agent Framework with LLM Integration

An intelligent agent framework built with LangChain that integrates multiple language models and useful tools for versatile task automation and information retrieval.

## 🚀 Features

- **Multiple LLM Support**: Seamlessly switch between Groq (DeepSeek R1 Distill LLaMa 70B) and Google Gemini 2.0 Flash models
- **Conversational Memory**: Maintains context throughout interactions using ConversationBufferMemory
- **Interactive CLI Interface**: Simple command-line interface for easy interaction
- **Integrated Tools Suite**:
  - Web search capabilities via DuckDuckGo
  - Python code execution in real-time
  - Safe shell command execution with security protections
  - File operations (search, read, write)


## 🔧 Installation

1. Clone this repository:
```bash
git clone https://github.com/BEASTBOYJAY/MultiTool-AI-Agent.git
cd MultiTool-AI-Agent
```

2. Install uv If not already installed:
```bash
pip install uv
```


3. Install the required dependencies:
```bash
uv pip install .
```

4. Set up your API keys as environment variables:
```bash
export GOOGLE_API_KEY="your_google_api_key"
export GROQ_API_KEY="your_groq_api_key"
```

## 📝 Project Structure

```
.
├── main.py              # Main application entry point
├── source/
│   ├── llm.py           # LLM model implementations
│   └── tools.py         # Tool implementations (search, shell, file operations)
└── README.md            # This documentation
```

## 🚀 Usage

Run the agent with:

```bash
python main.py
```

By default, the agent will use the Groq model. To use Google Gemini instead, modify the model type in `main.py`:

```python
if __name__ == "__main__":
    agent = Agent(model_type="gemini")  # Change from "groq" to "gemini"
    agent.run()
```

### Example Interactions

```
Ask your AI agent: What's the weather in New York?
Ask your AI agent: Write a Python function to calculate Fibonacci numbers
Ask your AI agent: Search for recent news about artificial intelligence
Ask your AI agent: Create a file named hello.py with a simple hello world program
```

To exit the application, type `exit`, `quit`, or `bye`.

## 🔒 Safety Features

The agent includes several safety features:
- Dangerous shell commands are automatically blocked
- Error handling for failed operations
- Structured reasoning pattern for transparent decision-making

## 🛠️ Available Tools

| Tool | Description |
|------|-------------|
| `DuckDuckGoSearchRun` | Search the web for real-time information |
| `PythonREPL` | Execute Python code on the fly |
| `SafeShellTool` | Run shell commands with built-in safety restrictions |
| `FileSearchTool` | Search for files in the system |
| `FileReadTool` | Read the contents of files |
| `FileWriteTool` | Write or create files with specified content |

## 🤖 How It Works

The agent uses the ReAct (Reasoning and Acting) pattern to:
1. Think about what to do based on your query
2. Choose appropriate tools to use
3. Execute tool actions to gather information
4. Continue reasoning until it can provide a final answer

The prompt template guides the agent through this process in a structured way, maintaining conversation history for contextual awareness.


## ⚠️ Limitations

- The agent's capabilities are limited by the available tools
- Some shell commands are intentionally blocked for safety
- Internet search results depend on DuckDuckGo's availability and results quality
- Response quality depends on the selected LLM model