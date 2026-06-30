import secrets
import hashlib

def generate_secret(length:int=32)->str:
    return secrets.token_hex(length)

def sha256(text:str)->str:
    return hashlib.sha256(text.encode()).hexdigest()

def mask_api_key(key:str)->str:
    if len(key)<=8:
        return "*"*len(key)
    return key[:4]+"*"*(len(key)-8)+key[-4:]
