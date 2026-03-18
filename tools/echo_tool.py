from tools.base_tool import BaseTool

class EchoTool(BaseTool):
    name = "ECHO"

    def execute(self, payload: dict) -> dict:
        if "message" not in payload:
            raise ValueError("Missing 'message' in payload")
        message = payload["message"]
        if not isinstance(message, str):
            raise ValueError("'message' must be a string")
        return {"echo": message}