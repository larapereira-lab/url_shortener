from fastapi import FastAPI, Request, Form
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from supabase_client import supabase
from utils import gerar_hash
import os

app = FastAPI()

# Diretórios já estão dentro de /app no container, então NÃO use "app/static"
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})




@app.post("/shorten", response_class=HTMLResponse)
def shorten(request: Request, url: str = Form(...)):
    hash = gerar_hash()

    supabase.table("urls").insert({
        "original_url": url,
        "short_hash": hash
    }).execute()

    base_url = os.getenv("BASE_URL", "http://localhost:8000/")
    short_url = f"{base_url}{hash}"
    return templates.TemplateResponse("index.html", {"request": request, "short_url": short_url})


@app.get("/{hash}")
def redirecionar(hash: str):
    response = supabase.table("urls").select("original_url").eq("short_hash", hash).single().execute()

    if response.data:
        return RedirectResponse(response.data["original_url"])

    return {"erro": "URL não encontrada"}
