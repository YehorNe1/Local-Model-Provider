# api_app.py
import random
from fastapi import FastAPI
from langchain.chains import LLMChain
from langchain.prompts import SystemMessagePromptTemplate, HumanMessagePromptTemplate, ChatPromptTemplate

from models import (
    CodeSnippetModel,
    ExplainResponseModel,
    GenerateRequestModel,
    GenerateResponseModel,
    TranslateRequestModel,
    TranslateResponseModel,
    StylePrefsModel
)
from style_manager import load_style_prefs, save_style_prefs
from tools import detect_code_language
from llm_providers import llm_generate, llm_explain_translate

app = FastAPI()

prompt_generate = """You are a coding assistant. Generate code in the requested language based on the user description.
Incorporate the user's style preferences if they exist."""

prompt_explain = """You are a coding assistant. Explain this code to a human, mentioning potential issues or edge cases."""

prompt_translate = """You are a coding assistant. Translate code from one language to another."""

@app.post("/generate_code", response_model=GenerateResponseModel)
def generate_code_endpoint(req: GenerateRequestModel):
    style = load_style_prefs()
    examples = [
        {
            "desc": "A function that prints 'Hello World'",
            "code": "def hello_world():\n    print('Hello World')"
        },
        {
            "desc": "A function that multiplies two numbers",
            "code": "def multiply_nums(a, b):\n    return a * b"
        },
        {
            "desc": "A function that checks if a number is prime",
            "code": """def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n**0.5)+1):
        if n % i == 0:
            return False
    return True
"""
        }
    ]
    random_example = random.choice(examples)

    chain_gen = LLMChain(
        llm=llm_generate,
        prompt=ChatPromptTemplate.from_messages([
            SystemMessagePromptTemplate.from_template(prompt_generate),
            HumanMessagePromptTemplate.from_template(
                "Style prefs: {style}\n"
                "Example:\n"
                "Description: {ex_desc}\n"
                "Code:\n{ex_code}\n\n"
                "Now generate code in {language} for:\n{desc}"
            )
        ])
    )

    result = chain_gen.run(
        style=style,
        ex_desc=random_example["desc"],
        ex_code=random_example["code"],
        language=req.language,
        desc=req.description
    )
    return GenerateResponseModel(code=result)

@app.post("/explain_code", response_model=ExplainResponseModel)
def explain_code_endpoint(req: CodeSnippetModel):
    snippet = req.snippet
    detected_lang = detect_code_language(snippet)

    chain_explain = LLMChain(
        llm=llm_explain_translate,
        prompt=ChatPromptTemplate.from_messages([
            SystemMessagePromptTemplate.from_template(prompt_explain),
            HumanMessagePromptTemplate.from_template(
                "This code is in {lang}:\n{code}\nExplain it clearly."
            )
        ])
    )

    explanation = chain_explain.run(lang=detected_lang, code=snippet)
    return ExplainResponseModel(explanation=explanation, language=detected_lang)

@app.post("/translate_code", response_model=TranslateResponseModel)
def translate_code_endpoint(req: TranslateRequestModel):
    snippet = req.snippet
    target_lang = req.target_language
    orig_lang = detect_code_language(snippet)

    chain_trans = LLMChain(
        llm=llm_explain_translate,
        prompt=ChatPromptTemplate.from_messages([
            SystemMessagePromptTemplate.from_template(prompt_translate),
            HumanMessagePromptTemplate.from_template(
                "Code is in {orig_lang}. Translate it to {tgt_lang}:\n{code}"
            )
        ])
    )

    translated = chain_trans.run(
        orig_lang=orig_lang,
        tgt_lang=target_lang,
        code=snippet
    )
    return TranslateResponseModel(
        original_language=orig_lang,
        translated_code=translated
    )

@app.post("/style_preferences")
def style_prefs_endpoint(prefs: StylePrefsModel):
    current = load_style_prefs()
    if prefs.indent_size is not None:
        current["indent_size"] = prefs.indent_size
    if prefs.naming_convention is not None:
        current["naming_convention"] = prefs.naming_convention
    save_style_prefs(current)
    return {"detail": "Style preferences updated", "current_prefs": current}