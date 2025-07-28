# shared/auth/auth_utils.py

import os
from fastapi import Request, HTTPException

INTERNAL_TOKEN = os.getenv("INTERNAL_SERVICE_TOKEN")

def verify_internal_token(request: Request):
    """Verifies Bearer token for internal service calls."""
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    token = auth_header.split(" ")[1]
    if token != INTERNAL_TOKEN:
        raise HTTPException(status_code=403, detail="Forbidden")
    return True
