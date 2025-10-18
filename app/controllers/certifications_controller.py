"""Certifications endpoints."""

from fastapi import APIRouter, Depends

from app.core.middleware import verify_api_key
from app.models.schemas import CertificationsResponse
from app.services.data_service import get_certifications

router = APIRouter(prefix="/v1/certifications", tags=["Certifications"], dependencies=[Depends(verify_api_key)])


@router.get("", response_model=CertificationsResponse)
async def list_certifications() -> CertificationsResponse:
    data = get_certifications()
    return CertificationsResponse(**data)
