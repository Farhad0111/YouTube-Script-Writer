from pydantic import BaseModel, Field
from typing import Optional, List

class ScriptRequest(BaseModel):
    topic: str
    tone: Optional[str] = "Informative"
    style: Optional[str] = "Conversational"
    duration: Optional[int] = 5  # in minutes
    audience: Optional[str] = "General"
    language: Optional[str] = "English"
    notes: Optional[str] = ""
    
class YouTubeChannelRequest(BaseModel):
    channel_id: str
    topic: str
    style: Optional[str] = "Conversational"
    duration: Optional[int] = 5  # in minutes
    audience: Optional[str] = "General"
    language: Optional[str] = "English"
    notes: Optional[str] = ""
    
class ChannelInfo(BaseModel):
    id: str
    title: str
    description: str
    customUrl: Optional[str] = ""
    publishedAt: str
    viewCount: int
    subscriberCount: int
    videoCount: int
    keywords: Optional[str] = ""
    videos: List[dict] = []
    
class ToneAnalysisResult(BaseModel):
    primary_tone: str
    secondary_tones: List[str] = []