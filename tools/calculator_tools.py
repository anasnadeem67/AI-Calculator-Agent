"""
tools/calculator_tools.py
──────────────────────────────────────────────────────
All calculator tools + CalculationMemory class.
Memory is managed via Streamlit session_state (passed in from ui/app.py).
"""

import json
import math
from dataclasses import dataclass, field
from typing import List

from agents import function_tool


# ─────────────────────────────────────────────
# MEMORY CLASS
# ─────────────────────────────────────────────

@dataclass
class CalculationMemory:
    history: List[dict] = field(default_factory=list)
    last_result: float = 0.0

    def add(self, expression: str, result: float):
        self.history.append({"expression": expression, "result": result})
        self.last_result = result


# ─────────────────────────────────────────────
# TOOLS
# ─────────────────────────────────────────────

# Memory reference — will be set by ui/app.py before use
_memory: CalculationMemory = CalculationMemory()


def set_memory(mem: CalculationMemory):
    """Called from app.py to inject the session-state memory object."""
    global _memory
    _memory = mem


@function_tool
def basic_calculate(expression: str) -> str:
    """Perform basic math like +, -, *, /, %. Use 'ans' for last result."""
    try:
        expr_to_eval = expression.lower().replace("ans", str(_memory.last_result))

        allowed = set("0123456789+-*/().% e")
        if not all(c in allowed for c in expr_to_eval):
            return json.dumps({"error": "Invalid characters detected", "status": "error"})

        result = eval(expr_to_eval)
        _memory.add(expression, result)
        return json.dumps({"operation": expression, "result": result, "status": "success"})
    except Exception as e:
        return json.dumps({"error": str(e), "status": "error"})


@function_tool
def scientific_calculate(operation: str, value: float) -> str:
    """Scientific ops: sqrt, sin, cos, tan, log. Value in degrees for trig."""
    try:
        ops = {
            "sqrt": math.sqrt,
            "sin":  lambda x: math.sin(math.radians(x)),
            "cos":  lambda x: math.cos(math.radians(x)),
            "tan":  lambda x: math.tan(math.radians(x)),
            "log":  math.log,
        }
        if operation not in ops:
            return json.dumps({"error": "Unsupported operation", "status": "error"})

        result = ops[operation](value)
        _memory.add(f"{operation}({value})", result)
        return json.dumps({"operation": operation, "input": value, "result": result, "status": "success"})
    except Exception as e:
        return json.dumps({"error": str(e), "status": "error"})


@function_tool
def unit_convert(value: float, from_unit: str, to_unit: str) -> str:
    """Convert units: km to miles, kg to pounds, and vice versa."""
    conversions = {
        ("km",     "miles"):  lambda x: x * 0.621371,
        ("miles",  "km"):     lambda x: x * 1.60934,
        ("kg",     "pounds"): lambda x: x * 2.20462,
        ("pounds", "kg"):     lambda x: x * 0.453592,
    }
    key = (from_unit.lower(), to_unit.lower())
    try:
        if key not in conversions:
            return json.dumps({"error": "Conversion not supported", "status": "error"})
        result = conversions[key](value)
        _memory.add(f"{value}{from_unit} to {to_unit}", result)
        return json.dumps({"from": from_unit, "to": to_unit, "result": round(result, 2), "status": "success"})
    except Exception as e:
        return json.dumps({"error": str(e), "status": "error"})


@function_tool
def get_history(dummy: str = "") -> str:
    """Retrieve the last 5 calculations from memory. Pass empty string for dummy."""
    return json.dumps({"history": _memory.history[-5:], "last_ans": _memory.last_result})


ALL_TOOLS = [basic_calculate, scientific_calculate, unit_convert, get_history]
