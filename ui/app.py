"""
ui/app.py
──────────────────────────────────────────────────────
Streamlit UI for the Agentic Calculator.
Run with: streamlit run ui/app.py
"""

import sys
import os
import asyncio
import streamlit as st
from agents import Runner

# Fix path for Streamlit Cloud — project root ko sys.path mein add karo
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from agent.core import build_agent, get_model_name
from tools.calculator_tools import CalculationMemory, set_memory

# ─────────────────────────────────────────────
# SESSION STATE INIT
# ─────────────────────────────────────────────

if "calc_memory" not in st.session_state:
    st.session_state.calc_memory = CalculationMemory()

if "messages" not in st.session_state:
    st.session_state.messages = []

# Inject session memory into tools module
set_memory(st.session_state.calc_memory)

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────

st.set_page_config(page_title="Agentic Calculator", layout="centered")
st.title("🤖 Agentic Calculator")
st.info(f"Model: `{get_model_name()}` via Groq")

# ─────────────────────────────────────────────
# CHAT HISTORY
# ─────────────────────────────────────────────

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# ─────────────────────────────────────────────
# USER INPUT
# ─────────────────────────────────────────────

if prompt := st.chat_input("Ask me a calculation (e.g., 'sqrt of 144' or 'ans + 10')"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    async def call_agent():
        agent = build_agent()
        return await Runner.run(agent, prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = asyncio.run(call_agent())
            final_text = response.final_output
            st.write(final_text)
            st.session_state.messages.append({"role": "assistant", "content": final_text})

# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────

with st.sidebar:
    st.header("🧠 Memory Status")
    mem = st.session_state.calc_memory
    st.write(f"**Last Result (ans):** `{mem.last_result}`")

    if mem.history:
        st.subheader("Recent Calculations")
        for entry in reversed(mem.history[-5:]):
            st.write(f"• `{entry['expression']}` = **{entry['result']}**")

    if st.button("🗑️ Clear Memory"):
        st.session_state.calc_memory = CalculationMemory()
        set_memory(st.session_state.calc_memory)
        st.rerun()
