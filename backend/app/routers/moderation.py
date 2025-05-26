from fastapi import APIRouter, Depends
from ..models import ModerationRequest, ModerationResponse
from ..dependencies import verify_token
from ..moderation import moderate_image


router = APIRouter()


@router.post("/", response_model=ModerationResponse)
async def moderate_endpoint(
    request: ModerationRequest,
    token_doc: dict = Depends(verify_token)
):
    result = moderate_image(request.image_url)
    return result