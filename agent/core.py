"""
agent/core.py
──────────────────────────────────────────────────────
Calculator Agent setup using OpenAI Agents SDK.
Uses Groq as backend (OpenAI-compatible API).
"""

import os
from openai import AsyncOpenAI
from agents import Agent, ModelSettings
from agents.models.openai_chatcompletions import OpenAIChatCompletionsModel

from tools.calculator_tools import ALL_TOOLS


def _get(key: str, default: str = "") -> str:
    """Read from Streamlit secrets (cloud) or environment variables (local)."""
    try:
        import streamlit as st
        return st.secrets.get(key, os.getenv(key, default))
    except Exception:
        return os.getenv(key, default)


def build_agent() -> Agent:
    """Creates the calculator agent with Groq backend."""
    client = AsyncOpenAI(
        api_key=_get("GROQ_API_KEY"),
        base_url=_get("BASE_URL", "https://api.groq.com/openai/v1"),
        max_retries=0,
    )
    model = OpenAIChatCompletionsModel(
        model=_get("MODEL", "llama-3.3-70b-versatile"),
        openai_client=client,
    )
    return Agent(
        name="ProCalculator",
        instructions="""You are a professional Calculator Agent.
        - Use 'basic_calculate' for simple math (+, -, *, /, %).
        - Use 'scientific_calculate' for sqrt, sin, cos, tan, log.
        - Use 'unit_convert' for measurements (km/miles, kg/pounds).
        - If user asks for history or previous work, use 'get_history'.
        - ALWAYS provide a final answer based on tool output.""",
        tools=ALL_TOOLS,
        model=model,
        model_settings=ModelSettings(
            max_tokens=int(_get("MAX_TOKENS", "512")),
        ),
    )


def get_model_name() -> str:
    return _get("MODEL", "llama-3.3-70b-versatile")

def get_max_tokens() -> int:
    return int(_get("MAX_TOKENS", "512"))
