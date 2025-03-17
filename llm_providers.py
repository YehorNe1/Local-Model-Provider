# llm_providers.py
from langchain.llms import Ollama

# Model for code generation
llm_generate = Ollama(
    base_url="http://localhost:11434",
    model="gemma:2b"
)

# Model for explaining and translating
llm_explain_translate = Ollama(
    base_url="http://localhost:11434",
    model="llama3.2:latest"
)