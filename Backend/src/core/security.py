from fastapi import HTTPException,APIRouter,Request
import os


def validate_api_key(request):
    header_key=request.headers.get('X-API-Key')

    correct_key= os.getenv("API_KEY")

    if not header_key:
        
        raise HTTPException(status_code=401,detail="Missing API key")
    
    if header_key != correct_key:
        raise HTTPException(status_code=403,detail="Invalid API key")
    
    return None