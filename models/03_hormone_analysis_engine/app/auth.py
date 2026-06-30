from fastapi import Header,HTTPException
from app.config import settings
async def verify_api_key(x_api_key:str=Header(default="")):
    if getattr(settings,"SECRET_KEY","") and x_api_key!=settings.SECRET_KEY:
        raise HTTPException(status_code=401,detail="Invalid API key")
