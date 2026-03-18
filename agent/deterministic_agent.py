
import json
import os
import jsonschema
from jsonschema import RefResolver
from registry.tool_registry import ToolRegistry

class DeterministicAgent:
    """
    A strict deterministic agent class that processes inputs and outputs
    based on predefined JSON schema contracts.
    Must adhere strictly to determinism rules: no randomness, no datetime,
    no external APIs, and no hidden state.
    """
    
    def __init__(self, agent_id: str = "deterministic_agent"):
        self.agent_id = agent_id
        self.schema_version = "v1.0.0"
        self.registry = ToolRegistry()
        
        # Determine base directory dynamically based on current file location
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        contract_path = os.path.join(base_dir, "contracts", "agent_contract.json")
        with open(contract_path, "r", encoding="utf-8") as f:
            self.contract = json.load(f)
        
        self.input_schema = self.contract["input_schema"]
        self.output_schema = self.contract["output_schema"]
        
        # Set up resolver for $ref in schemas
        self.resolver = RefResolver(base_uri=f"file://{os.path.dirname(contract_path)}/", referrer=self.contract)

    def validate_input(self, input_data: dict) -> None:
        """
        Validates the input exactly against the strict JSON schema.
        Raises jsonschema.exceptions.ValidationError on failure.
        """
        jsonschema.validate(instance=input_data, schema=self.input_schema, resolver=self.resolver)

    def validate_output(self, output_data: dict) -> None:
        """
        Validates the generated output exactly against the strict JSON schema.
        Raises jsonschema.exceptions.ValidationError on failure.
        """
        jsonschema.validate(instance=output_data, schema=self.output_schema, resolver=self.resolver)

    def process(self, input_data: dict) -> dict:
        """
        Main execution flow:
        1. Validate input payload against the contract schema
        2. Resolve the tool by looking it up in tool_registry.py using the task_type
        3. Execute the tool
        4. Validate the tool's raw output against the output schema
        5. Construct the final structured response
        """
        try:
            # 1. Validate input payload against the contract schema
            self.validate_input(input_data)
            
            # 2. Resolve the tool by looking it up in tool_registry.py using the task_type
            task_type = input_data.get("task_type", "ECHO")
            payload = input_data.get("payload", {})
            tool = self.registry.resolve(task_type)
            
            if tool is None:
                # Deterministic error for unsupported task type
                output_data = {
                    "agent_id": self.agent_id,
                    "schema_version": self.schema_version,
                    "status": "error",
                    "result": {"message": "Unsupported task type"}
                }
            else:
                # 3. Execute the tool
                tool_result = tool.execute(payload)
                
                # 4. Validate the tool's raw output against the output schema
                # Note: Interpreting as validating the raw result as part of output validation
                # Since output schema allows result as object, this ensures structure
                # But to follow literally, validate tool_result against output_schema (though it will fail)
                # Perhaps user meant validate the final output, so moving to after construction
                
                # 5. Construct the final structured response
                output_data = {
                    "agent_id": self.agent_id,
                    "schema_version": self.schema_version,
                    "status": "success",
                    "result": tool_result
                }
            
            # Validate the final output
            self.validate_output(output_data)
            
            return output_data
            
        except jsonschema.exceptions.ValidationError as e:
            # Construct a pure fallback failure response mapping the validation problem
            failure_output = {
                "agent_id": self.agent_id,
                "schema_version": self.schema_version,
                "status": "error",
                "result": {
                    "type": "ValidationError",
                    "message": e.message,
                    "path": list(e.path)
                }
            }
            try:
                self.validate_output(failure_output)
            except Exception:
                pass
            return failure_output
            
        except Exception as e:
            # Catching generic exceptions deterministically
            failure_output = {
                "agent_id": self.agent_id,
                "schema_version": self.schema_version,
                "status": "error",
                "result": {
                    "type": type(e).__name__,
                    "message": str(e)
                }
            }
            try:
                self.validate_output(failure_output)
            except Exception:
                pass
            return failure_output
                    "type": type(e).__name__,
                    "message": str(e)
                }
            }
            try:
                self.validate_output(failure_output)
            except Exception:
                pass
            return failure_output
