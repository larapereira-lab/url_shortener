import os
from supabase import create_client

from dotenv import load_dotenv
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def gerar_hash():
    import random, string
    return ''.join(random.choices(string.ascii_letters + string.digits, k=6))

