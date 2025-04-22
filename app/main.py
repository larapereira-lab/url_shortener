from fastapi import FastAPI, Request, Form
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os
from database import supabase, gerar_hash

app = FastAPI()

# Corrigido o caminho dos diretórios
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/shorten", response_class=HTMLResponse)
def shorten(request: Request, url: str = Form(...)):
    hash = gerar_hash()
    supabase.table("urls").insert({"original_url": url, "short_hash": hash}).execute()
    short_url = os.getenv("BASE_URL") + hash
    return templates.TemplateResponse("index.html", {"request": request, "short_url": short_url})

@app.get("/{hash}")
def redirecionar(hash: str):
    result = supabase.table("urls").select("original_url").eq("short_hash", hash).single().execute()
    if result.data:
        return RedirectResponse(result.data["original_url"])
    return {"erro": "URL não encontrada"}

