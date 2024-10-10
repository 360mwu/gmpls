from fastapi import Request
from fastapi.responses import RedirectResponse
from starlette.middleware.base import BaseHTTPMiddleware
from pydantic import ValidationError
from app.models.local import LocalConfigCheck
import os
import json

class InstallMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        config_path = 'app/database/local.json'
        
        if request.url.path.startswith("/static"):
            return await call_next(request)

        if request.method == "POST" and request.url.path in ["/check_db_connection", "/go_install"]:
            return await call_next(request)
        
        if os.path.exists(config_path):
            with open(config_path, 'r') as f:
                try:
                    config_data = json.load(f)
                    config = LocalConfigCheck(**config_data)

                    if request.url.path == "/install":
                        return RedirectResponse("/")
                except (ValidationError, json.JSONDecodeError):
                    if request.url.path != "/install":
                        return RedirectResponse("/install")  
        else:
            if request.url.path != "/install":
                return RedirectResponse("/install")  
        
        response = await call_next(request)
        return response