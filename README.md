# Deterministic Agent Framework

A strict deterministic agent framework that executes tasks through a **registry-driven tool execution pipeline**. The agent is deterministic: no randomness, no timestamps, no external services, and no hidden state.

## ✅ Project Overview

This repository implements a **deterministic agent execution framework** where:
- Input is validated against a **strict JSON schema**
- The agent looks up a tool in a **registry** based on `task_type`
- The selected tool executes deterministically and returns a structured result
- Output is validated against a strict JSON schema

## 🧩 Architecture (Registry-Based)

### Core components
- `agent/deterministic_agent.py` — Main agent execution flow
- `registry/tool_registry.py` — Maps `task_type` → tool class
- `tools/` — Individual tool implementations
- `schemas/` — JSON schema contracts for input/output
- `contracts/agent_contract.json` — Agent guarantees description

## 🔁 Execution Flow

Input → `agent.process(input_data)`
↓
Input JSON Schema Validation
↓
Registry Resolution (`self.registry.resolve(task_type)`)
↓
Tool Execution (`tool.execute(payload)`)
↓
Agent Wrapper (Appending `status`, `schema_version`, `agent_id`)
↓
Output JSON Schema Validation
↓
Return JSON String

## 🎯 Deterministic Guarantees

This project guarantees deterministic behavior by ensuring:
- No randomness (no `random`, no UUIDs)
- No datetime-based values
- No external API calls natively or dependencies mapping to external endpoints
- No hidden mutable state or global registries preserving values between calls
- Same json input produces identical bit-for-bit json matching output every single time

## ▶️ How to Run the Demo

```bash
python run_demo.py
```

## 🧪 How to Run Tests

```bash
python -m unittest
```

## 🧰 Adding a New Tool

1. Create a new tool class in `tools/` inheriting from `BaseTool`.
2. Implement `execute(self, payload: dict) -> dict` and return only the raw data wrapped in a "result" key:

```python
{
  "result": { ... }
}
```
*Note: The DeterministicAgent handles wrapping this output with the standard contract payload (`schema_version`, `status`, `agent_id`, etc).*

3. Register the tool in `registry/tool_registry.py`:

```python
from tools.my_tool import MyTool

TOOL_REGISTRY = {
    "MY_TASK": MyTool,
    # ...
}
```

4. Add tests in `tests/test_agent.py` to validate deterministic output.
