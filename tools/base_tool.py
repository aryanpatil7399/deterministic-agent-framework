class BaseTool:
    name = ""

    def execute(self, payload: dict) -> dict:
        raise NotImplementedError("Tool must implement execute()")