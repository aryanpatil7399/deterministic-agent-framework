from tools.echo_tool import EchoTool
from tools.sum_numbers_tool import SumNumbersTool
from tools.uppercase_text_tool import UppercaseTextTool

TOOL_REGISTRY = {
    "ECHO": EchoTool,
    "SUM_NUMBERS": SumNumbersTool,
    "UPPERCASE_TEXT": UppercaseTextTool
}

class ToolRegistry:
    def resolve(self, task_type: str):
        tool_class = TOOL_REGISTRY.get(task_type)
        if tool_class is not None:
            return tool_class()
        return None