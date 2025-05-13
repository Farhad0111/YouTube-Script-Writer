from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from groq_client import get_script
from prompts import build_prompt
from models import ScriptRequest, YouTubeChannelRequest, ChannelInfo, ToneAnalysisResult
from youtube_client import YouTubeClient
from tone_analyzer import ToneAnalyzer
import json

app = FastAPI()

# Mount static and template folders
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Initialize clients
youtube_client = YouTubeClient()
tone_analyzer = ToneAnalyzer()


@app.get("/", response_class=HTMLResponse)
async def form_page(request: Request):
    """Render the main page with the script generation form"""
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/generate", response_class=HTMLResponse)
async def generate_script_view(
    request: Request,
    topic: str = Form(...),
    tone: str = Form("Informative"),
    style: str = Form("Conversational"),
    duration: int = Form(5),
    audience: str = Form("General"),
    language: str = Form("English"),
    notes: str = Form("")
):
    """Generate a script using the provided form parameters"""
    data = ScriptRequest(
        topic=topic,
        tone=tone,
        style=style,
        duration=duration,
        audience=audience,
        language=language,
        notes=notes
    )
    try:
        prompt = build_prompt(data)
        result = await get_script(prompt)
        return templates.TemplateResponse("index.html", {
            "request": request, 
            "script": result,
            "form_data": data.dict()
        })
    except Exception as e:
        error_message = f"Error generating script: {str(e)}"
        return templates.TemplateResponse("index.html", {
            "request": request,
            "error": error_message,
            "form_data": data.dict()
        })


@app.post("/generate-from-channel", response_class=HTMLResponse)
async def generate_from_channel_view(
    request: Request,
    channel_id: str = Form(...),
    topic: str = Form(...),
    style: str = Form("Conversational"),
    duration: int = Form(5),
    audience: str = Form("General"),
    language: str = Form("English"),
    notes: str = Form("")
):
    """Generate a script using the tone derived from a YouTube channel"""
    try:
        # Get channel info
        channel_data = youtube_client.get_channel_info(channel_id)
        if not channel_data:
            raise HTTPException(status_code=404, detail="Channel not found")
        
        # Analyze tone
        primary_tone = tone_analyzer.analyze_channel_tone(channel_data)
        secondary_tones = tone_analyzer.get_secondary_tones(channel_data)
        
        # Create script request with channel tone
        data = ScriptRequest(
            topic=topic,
            tone=primary_tone,
            style=style,
            duration=duration,
            audience=audience,
            language=language,
            notes=notes
        )
        
        # Generate script
        prompt = build_prompt(data)
        result = await get_script(prompt)
        
        # Prepare channel info for template
        channel_info = {
            "title": channel_data.get("title", ""),
            "description": channel_data.get("description", ""),
            "subscribers": channel_data.get("subscriberCount", 0),
            "videos": channel_data.get("videoCount", 0),
            "primary_tone": primary_tone,
            "secondary_tones": secondary_tones
        }
        
        return templates.TemplateResponse("index.html", {
            "request": request, 
            "script": result,
            "form_data": data.dict(),
            "channel_info": channel_info,
            "channel_id": channel_id
        })
    except HTTPException as he:
        return templates.TemplateResponse("index.html", {
            "request": request,
            "error": he.detail,
            "form_data": {
                "topic": topic,
                "style": style,
                "duration": duration,
                "audience": audience,
                "language": language,
                "notes": notes
            },
            "channel_id": channel_id
        })
    except Exception as e:
        error_message = f"Error processing request: {str(e)}"
        return templates.TemplateResponse("index.html", {
            "request": request,
            "error": error_message,
            "form_data": {
                "topic": topic,
                "style": style,
                "duration": duration,
                "audience": audience,
                "language": language,
                "notes": notes
            },
            "channel_id": channel_id
        })


@app.get("/api/channel-info/{channel_id}", response_class=JSONResponse)
async def get_channel_info_api(channel_id: str):
    """API endpoint to get channel info and tone analysis"""
    try:
        channel_data = youtube_client.get_channel_info(channel_id)
        if not channel_data:
            raise HTTPException(status_code=404, detail="Channel not found")
        
        primary_tone = tone_analyzer.analyze_channel_tone(channel_data)
        secondary_tones = tone_analyzer.get_secondary_tones(channel_data)
        
        return {
            "channel": {
                "id": channel_data.get("id", ""),
                "title": channel_data.get("title", ""),
                "description": channel_data.get("description", ""),
                "subscribers": channel_data.get("subscriberCount", 0),
                "videos": channel_data.get("videoCount", 0)
            },
            "tones": {
                "primary": primary_tone,
                "secondary": secondary_tones
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))