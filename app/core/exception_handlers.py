# app/core/exception_handlers.py
from fastapi.responses import JSONResponse
from fastapi import Request, HTTPException

async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "status": "failure",
            "message": exc.detail,
            "data": None
        },
    )
