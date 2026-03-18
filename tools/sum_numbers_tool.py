from tools.base_tool import BaseTool

class SumNumbersTool(BaseTool):
    name = "SUM_NUMBERS"

    def execute(self, payload: dict) -> dict:
        if "numbers" not in payload:
            raise ValueError("Missing 'numbers' in payload")
        numbers = payload["numbers"]
        if not isinstance(numbers, list):
            raise ValueError("'numbers' must be a list")
        try:
            total = sum(numbers)
            return {"sum": total}
        except TypeError:
            raise ValueError("All items in 'numbers' must be numeric")