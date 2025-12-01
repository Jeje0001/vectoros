import time,typing

from fastapi import HTTPException

Rate_limit_per_minute=60
Window_seconds=60
requests_per_key: dict[str,dict]={}


def check_rate_limit(api_key: str) -> None:
    if api_key in (None,""):
        raise HTTPException(status_code=401,detail="Api key cant be empty")
    
    now= time.time()
    state=requests_per_key.get(api_key)

    if state is None or now - state["window_start"] >= Window_seconds:
        state={
            "window_start":now,
            "count":1
        }
        requests_per_key[api_key]=state
        return None
        
    
    state["count"]+=1

    if state["count"] > Rate_limit_per_minute:
        raise HTTPException(status_code=429, detail="Rate limit exceeded (60 requests per minute)")
    requests_per_key[api_key]=state
    return None
        