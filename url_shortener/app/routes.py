from fastapi import APIRouter, HTTPException, Request
from app.supabase_client import supabase
from app.utils import generate_short_code

router = APIRouter()

@router.post("/shorten")
async def shorten_url(request: Request):
    data = await request.json()
    original_url = data.get("url")

    if not original_url:
        raise HTTPException(status_code=400, detail="URL is required")

    short_code = generate_short_code()

    result = supabase.table("urls").insert({
        "original_url": original_url,
        "short_code": short_code
    }).execute()

    return {"shortened_url": f"https://yourdomain.com/{short_code}"}

@router.get("/{short_code}")
async def redirect_url(short_code: str):
    response = supabase.table("urls").select("original_url").eq("short_code", short_code).single().execute()

    if response.data is None:
        raise HTTPException(status_code=404, detail="URL not found")

    return {"original_url": response.data["original_url"]}