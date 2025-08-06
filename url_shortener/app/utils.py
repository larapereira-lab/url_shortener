import random
import string

def gerar_hash():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=6))
