from tools.base_tool import BaseTool

class UppercaseTextTool(BaseTool):
    name = "UPPERCASE_TEXT"

    def execute(self, payload: dict) -> dict:
        if "text" not in payload:
            raise ValueError("Missing 'text' in payload")
        text = payload["text"]
        if not isinstance(text, str):
            raise ValueError("'text' must be a string")
        return {"result": text.upper()}