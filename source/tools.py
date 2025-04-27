from langchain_community.tools import DuckDuckGoSearchRun, ShellTool
from langchain_experimental.utilities import PythonREPL
from langchain_core.tools import Tool, BaseTool
import re
from pydantic import Field

from langchain.tools import BaseTool
import os


class FileSearchTool(BaseTool):
    name: str = "file_search_tool"
    description: str = "A tool to search for files on the system."

    @staticmethod
    def search_files(query: str, search_dir: str = "/"):
        """Search for files in the system based on the query (file name or pattern)."""

        result = []

        for dirpath, _, filenames in os.walk(search_dir):
            for filename in filenames:
                if query.lower() in filename.lower():
                    result.append(os.path.join(dirpath, filename))

        return result

    def _run(self, query: str) -> str:
        """Execute the file search and return the results."""
        search_results = self.search_files(query)
        if search_results:
            return "\n".join(search_results)
        else:
            return "No files found matching the query."

    def _arun(self, query: str) -> str:
        """Asynchronous run, not used in this case."""
        return self._run(query)


class FileReadTool(BaseTool):
    name: str = "file_read_tool"
    description: str = "A tool to read the contents of a file."

    def _run(self, file_path: str) -> str:
        """Read the contents of a file."""
        try:
            with open(file_path, "r") as file:
                return file.read()
        except Exception as e:
            return f"Error reading file: {e}"

    def _arun(self, query: str) -> str:
        """Asynchronous run, not used in this case."""
        return self._run(query)


class SafeShellTool(BaseTool):
    name: str = "safe_shell_tool"
    description: str = (
        "Run safe shell commands on the machine. Dangerous commands are blocked automatically."
    )
    shell_tool: ShellTool = Field(default_factory=ShellTool)

    def __init__(self):
        super().__init__()
        self.shell_tool = ShellTool()

    def _run(self, query: str, **kwargs) -> str:
        banned_patterns = [
            r"\brm\b",
            r"\brmdir\b",
            r"\bmv\b",
            r"\bsudo\b",
            r"\bapt[\s-]*get\b",
            r"\byum\b",
            r"\bpip[\s]*install\b",
            r"\bconda[\s]*install\b",
            r"\bcurl\b",
            r"\bwget\b",
            r"\bchmod\b",
            r"\bchown\b",
        ]
        for pattern in banned_patterns:
            if re.search(pattern, query.lower()):
                return "⛔ Sorry, cannot execute this command."
        return self.shell_tool.run(query)

    def _arun(self, query: str, **kwargs) -> str:
        """Optional: async version (not required usually)"""
        raise NotImplementedError("Async not supported yet.")


class Tools:
    def __init__(self):
        # search tool
        self.search_tool = DuckDuckGoSearchRun()

        # python execution tool
        self.python_repl = PythonREPL()
        self.repl_tool = Tool(
            name="python_repl",
            description="A Python shell. Use this to execute python commands. Input should be a valid python command. If you want to see the output of a value, you should print it out with `print(...)`.",
            func=self.python_repl.run,
        )

        # shell tool
        self.shell_tool = SafeShellTool()
        self.file_search_tool = FileSearchTool()
        self.file_read_tool = FileReadTool()

    def run(self):

        return [
            self.search_tool,
            self.repl_tool,
            self.shell_tool,
            self.file_search_tool,
            self.file_read_tool,
        ]


if __name__ == "__main__":
    tools = Tools()
    print(tools.run())
