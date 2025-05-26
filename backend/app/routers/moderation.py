from fastapi import APIRouter, Depends
from ..models import ModerationRequest, ModerationResponse
from ..dependencies import verify_token
from ..moderation_service import check_image_safety


router = APIRouter()


@router.post("/", response_model=ModerationResponse)
async def moderate_endpoint(
    request: ModerationRequest,
    token_doc: dict = Depends(verify_token)
):
    result = await check_image_safety(request.image_url)
    return result
