from pydantic import BaseModel
from typing import Optional

class ScriptRequest(BaseModel):
    topic: str
    tone: Optional[str] = "Informative"
    style: Optional[str] = "Conversational"
    duration: Optional[int] = 5  # in minutes
    audience: Optional[str] = "General"
    language: Optional[str] = "English"
    notes: Optional[str] = ""
