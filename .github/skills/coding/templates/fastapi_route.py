"""FastAPI route scaffold — router with dependency injection."""

from fastapi import APIRouter, Depends, HTTPException, status

router = APIRouter(prefix="/items", tags=["items"])


@router.post("/", response_model=Item, status_code=status.HTTP_201_CREATED)
async def create_item(
    body: ItemCreate,
    service: ItemService = Depends(get_service),
) -> Item:
    try:
        return service.create(body)
    except DuplicateItemError as e:
        raise HTTPException(status_code=409, detail=str(e)) from e
