# 🤖 Agentic Calculator

A calculator agent built with **OpenAI Agents SDK** + **OpenRouter** backend, with a **Streamlit** chat UI.

## Folder Structure

```
calculator_agent/
├── .env                        ← API keys (never commit this)
├── .env.example                ← Template for .env
├── .gitignore
├── requirements.txt
├── README.md
├── agent/
│   ├── __init__.py
│   └── core.py                 ← Agent definition
├── tools/
│   ├── __init__.py
│   └── calculator_tools.py     ← All tools + Memory class
└── ui/
    └── app.py                  ← Streamlit UI
```

## Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure environment:**
   ```bash
   cp .env.example .env
   # Add your OPENROUTER_API_KEY in .env
   ```

3. **Run the app:**
   ```bash
   streamlit run ui/app.py
   ```

## Tools Available

| Tool | Description |
|------|-------------|
| `basic_calculate` | Basic math: +, -, *, /, % — supports `ans` for last result |
| `scientific_calculate` | sqrt, sin, cos, tan, log |
| `unit_convert` | km↔miles, kg↔pounds |
| `get_history` | Last 5 calculations |
