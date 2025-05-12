from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from groq_client import get_script
from prompts import build_prompt
from models import ScriptRequest

app = FastAPI()

# Mount static and template folders
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def form_page(request: Request):
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
    data = ScriptRequest(
        topic=topic,
        tone=tone,
        style=style,
        duration=duration,
        audience=audience,
        language=language,
        notes=notes
    )
    prompt = build_prompt(data)
    result = await get_script(prompt)
    return templates.TemplateResponse("index.html", {"request": request, "script": result})
