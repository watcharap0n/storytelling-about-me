"""Work / case study endpoints."""

from fastapi import APIRouter, Depends, HTTPException, Query

from app.core.middleware import verify_api_key
from app.models.schemas import WorkListResponse, WorkItem
from app.services.data_service import get_work_item, get_work_items

router = APIRouter(prefix="/v1/work", tags=["Work"], dependencies=[Depends(verify_api_key)])


@router.get("", response_model=WorkListResponse)
async def list_work(limit: int = Query(default=None, ge=1, le=20)) -> WorkListResponse:
    items = [WorkItem(**item) for item in get_work_items(limit=limit)]
    return WorkListResponse(items=items)


@router.get("/{slug}", response_model=WorkItem)
async def get_work(slug: str) -> WorkItem:
    item = get_work_item(slug)
    if not item:
        raise HTTPException(status_code=404, detail={"code": "ERR_NOT_FOUND", "message": "Work item not found."})
    return WorkItem(**item)
