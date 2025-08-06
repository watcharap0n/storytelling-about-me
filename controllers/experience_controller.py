"""API endpoints exposing career experiences."""
from fastapi import APIRouter
from models.experience import Experience
from services.mango_service import get_mango_experience

# Router grouping experience related endpoints
router = APIRouter(prefix="/experience", tags=["experience"])


@router.get("/mango", response_model=Experience)
def read_mango_experience() -> Experience:
    """GET /experience/mango - return Mango Consultant story."""
    return get_mango_experience()
