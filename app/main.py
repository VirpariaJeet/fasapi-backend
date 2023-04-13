import logging
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse
from fastapi.requests import Request
import time

from src.api.api_v1.api import api_router
from src.core.config import settings
from src.schemas import GenericResponse


logger = logging.getLogger(__name__)

app = FastAPI(
    title=settings.PROJECT_NAME, openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

@app.on_event("startup")
async def startup_event():
    logger.info("startup event!")

@app.on_event("shutdown")
async def shutdown_event():
    # TODO: graceful shutdown!!!?
    logger.info("Server shutdown!")


# TODO: move this to exception folder
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc: HTTPException):
    return JSONResponse(GenericResponse(success=False, description=str(exc.detail)).dict(), status_code=exc.status_code)

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)

    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    # TODO: add response to generic format if it is not.
    return response

# Set all CORS enabled origins
# if settings.BACKEND_CORS_ORIGINS:
#     app.add_middleware(
#         CORSMiddleware,
#         allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
#         allow_credentials=True,
#         allow_methods=["*"],
#         allow_headers=["*"],
#     )

@app.get("/")
async def test():
    return {"msg": "running healthy!"}

app.include_router(api_router, prefix=settings.API_V1_STR)
