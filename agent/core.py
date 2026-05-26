"""
agent/core.py
──────────────────────────────────────────────────────
Calculator Agent setup using OpenAI Agents SDK.
Uses Groq as backend (OpenAI-compatible API).
"""

import os
from dotenv import load_dotenv
from openai import AsyncOpenAI
from agents import Agent, ModelSettings
from agents.models.openai_chatcompletions import OpenAIChatCompletionsModel

from tools.calculator_tools import ALL_TOOLS

load_dotenv()


def build_agent() -> Agent:
    """Creates the calculator agent with Groq backend."""
    client = AsyncOpenAI(
        api_key=os.getenv("GROQ_API_KEY"),
        base_url=os.getenv("BASE_URL", "https://api.groq.com/openai/v1"),
        max_retries=0,
    )
    model = OpenAIChatCompletionsModel(
        model=os.getenv("MODEL", "llama-3.3-70b-versatile"),
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
            max_tokens=int(os.getenv("MAX_TOKENS", "512")),
            parallel_tool_calls=False,
        ),
    )


def get_model_name() -> str:
    return os.getenv("MODEL", "llama-3.3-70b-versatile")

def get_max_tokens() -> int:
    return int(os.getenv("MAX_TOKENS", "512"))
