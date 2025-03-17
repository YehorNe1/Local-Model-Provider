# models.py
from pydantic import BaseModel
from typing import Optional

class CodeSnippetModel(BaseModel):
    snippet: str

class ExplainResponseModel(BaseModel):
    explanation: str
    language: str

class GenerateRequestModel(BaseModel):
    description: str
    language: Optional[str] = "Python"

class GenerateResponseModel(BaseModel):
    code: str

class TranslateRequestModel(BaseModel):
    snippet: str
    target_language: str

class TranslateResponseModel(BaseModel):
    original_language: str
    translated_code: str

class StylePrefsModel(BaseModel):
    indent_size: Optional[int] = 4
    naming_convention: Optional[str] = "snake_case"