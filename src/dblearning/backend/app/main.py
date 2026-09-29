from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.api.api import api_router
from app.core.config import settings

app = FastAPI(
    title="DB Learning API",
    description="Hệ thống Cá nhân hóa Lộ trình Học tập môn Cơ sở Dữ liệu",
    version="1.0.0",
)

# Set all CORS enabled origins
if settings.cors_origins_list:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins_list,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(api_router, prefix="/api")

# Serve static files for document storage (PDFs, images)
# In production, Nginx will handle this. This is for dev fallback.
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def root():
    return {"message": "Welcome to DB Learning API. Check /docs for API documentation."}
