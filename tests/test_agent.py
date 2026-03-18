import os
import sys
import unittest

# Ensure the agent directory is in the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent.deterministic_agent import DeterministicAgent

class TestDeterministicAgent(unittest.TestCase):
    def setUp(self):
        self.agent = DeterministicAgent()

    def test_valid_input_echo(self):
        input_data = {
            "user_id": "test_user",
            "task_type": "ECHO",
            "payload": {
                "message": "Hello World"
            }
        }

        output = self.agent.process(input_data)

        self.assertEqual(output["status"], "success")
        self.assertEqual(output["agent_id"], "deterministic_agent")
        self.assertEqual(output["schema_version"], "v1.0.0")
        self.assertEqual(output["result"], {"result": "Hello World"})
        self.assertIn("result", output)

    def test_valid_input_sum_numbers(self):
        input_data = {
            "user_id": "test_user",
            "task_type": "SUM_NUMBERS",
            "payload": {
                "numbers": [1, 2, 3, 4, 5]
            }
        }

        output = self.agent.process(input_data)

        self.assertEqual(output["status"], "success")
        self.assertEqual(output["result"], {"result": 15})

    def test_valid_input_uppercase_text(self):
        input_data = {
            "user_id": "test_user",
            "task_type": "UPPERCASE_TEXT",
            "payload": {
                "text": "hello determinism"
            }
        }

        output = self.agent.process(input_data)

        self.assertEqual(output["status"], "success")
        self.assertEqual(output["result"], {"result": "HELLO DETERMINISM"})

    def test_invalid_schema_extra_field(self):
        # Schema enforces additionalProperties: false
        input_data = {
            "user_id": "test_user",
            "task_type": "ECHO",
            "payload": {},
            "extra_field": "not allowed"
        }

        output = self.agent.process(input_data)

        self.assertEqual(output["status"], "error")
        self.assertIn("result", output)
        self.assertEqual(output["result"]["type"], "ValidationError")

    def test_missing_required_field(self):
        # Missing 'user_id'
        input_data = {
            "task_type": "ECHO",
            "payload": {}
        }

        output = self.agent.process(input_data)

        self.assertEqual(output["status"], "error")
        self.assertIn("result", output)
        self.assertEqual(output["result"]["type"], "ValidationError")
        # Verify the failure output adheres to its own schema requirements by just existing with right status
        self.assertEqual(output["schema_version"], "v1.0.0")

    def test_determinism_same_input_twice(self):
        input_data = {
            "user_id": "determinist",
            "task_type": "SUM_NUMBERS",
            "payload": {
                "numbers": [10, 20, 30]
            }
        }

        output1 = self.agent.process(input_data)
        output2 = self.agent.process(input_data)

        # Python dictionary comparison is exact
        self.assertEqual(output1, output2)
        self.assertEqual(output1["status"], "success")
        self.assertEqual(output1["result"]["result"], 60)

    def test_unsupported_task_type(self):
        input_data = {
            "user_id": "test_user",
            "task_type": "RANDOM_TASK",
            "payload": {}
        }

        output = self.agent.process(input_data)

        self.assertEqual(output["status"], "error")
        self.assertIn("result", output)
        self.assertEqual(output["result"]["message"], "Unsupported task type: RANDOM_TASK")

    def test_registry_extension(self):
        from registry.tool_registry import TOOL_REGISTRY
        from tools.base_tool import BaseTool
        
        class MockTool(BaseTool):
            name = "MOCK_TOOL"
            def execute(self, payload: dict) -> dict:
                return {"result": f"Mocked {payload.get('val')}"}
                
        # Inject without touching DeterministicAgent
        TOOL_REGISTRY["MOCK_TOOL"] = MockTool
        
        input_data = {
            "user_id": "test",
            "task_type": "MOCK_TOOL",
            "payload": {"val": 99}
        }
        output = self.agent.process(input_data)
        self.assertEqual(output["status"], "success")
        self.assertEqual(output["result"], {"result": "Mocked 99"})

    def test_strict_determinism_5_times(self):
        import json
        input_data = {
            "user_id": "determinist",
            "task_type": "SUM_NUMBERS",
            "payload": {"numbers": [10, 20]}
        }
        
        outputs = []
        for _ in range(5):
            out = self.agent.process(input_data)
            outputs.append(json.dumps(out, sort_keys=True))
            
        for i in range(1, 5):
            self.assertEqual(outputs[0], outputs[i])
            
    def test_registry_returns_fresh_tool_instances(self):
        # Ensure tool executions are stateless via registry.
        tool1 = self.agent.registry.resolve("ECHO")
        tool2 = self.agent.registry.resolve("ECHO")
        self.assertIsNot(tool1, tool2)
        
        input_data = {
            "user_id": "determinist",
            "task_type": "ECHO",
            "payload": {"message": "hi"}
        }
        out1 = self.agent.process(input_data)
        out2 = self.agent.process(input_data)
        self.assertEqual(out1, out2)

if __name__ == '__main__':
    unittest.main()
