from fastapi import APIRouter

from app.api.endpoints import auth, learning, quiz, recommendation, admin

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(learning.router, prefix="/learning", tags=["learning"])
api_router.include_router(quiz.router, prefix="/quiz", tags=["quiz"])
api_router.include_router(recommendation.router, prefix="/recommendations", tags=["recommendations"])
api_router.include_router(admin.router, prefix="/admin", tags=["admin"])
