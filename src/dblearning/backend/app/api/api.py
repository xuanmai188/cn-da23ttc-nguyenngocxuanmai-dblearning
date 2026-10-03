from fastapi import APIRouter

from app.api.endpoints import auth, learning, quiz, recommendation, admin, student_survey, reports

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(learning.router, prefix="/learning", tags=["learning"])
api_router.include_router(quiz.router, prefix="/quiz", tags=["quiz"])
api_router.include_router(recommendation.router, prefix="/recommendations", tags=["recommendations"])
api_router.include_router(admin.router, prefix="/admin", tags=["admin"])
api_router.include_router(student_survey.router, prefix="/survey", tags=["survey"])

api_router.include_router(reports.router, prefix="/admin/reports", tags=["reports"])
