from fastapi import FastAPI, Request, Form, Depends
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from database import SessionLocal, get_db
from models import URL
from utils import gerar_hash
import os

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/shorten", response_class=HTMLResponse)
def shorten(
    request: Request,
    url: str = Form(...),
    db: Session = Depends(get_db)
):
    hash = gerar_hash()
    nova_url = URL(original_url=url, short_hash=hash)
    db.add(nova_url)
    db.commit()
    db.refresh(nova_url)

    short_url = os.getenv("BASE_URL", "http://localhost:8000/") + hash
    return templates.TemplateResponse("index.html", {"request": request, "short_url": short_url})


@app.get("/{hash}")
def redirecionar(hash: str, db: Session = Depends(get_db)):
    url = db.query(URL).filter(URL.short_hash == hash).first()
    if url:
        return RedirectResponse(url.original_url)
    return {"erro": "URL não encontrada"}

print("✅ URL_Shortener está no ar!")
