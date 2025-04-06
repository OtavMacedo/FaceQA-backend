from http import HTTPStatus

from fastapi import APIRouter, Depends

from app.core.security import get_current_user
from app.models.user import User
from app.schemas.api_key import APIKeySchema
from app.services.api_key_service import ApiKeyService

router = APIRouter(prefix='/api-keys', tags=['APIKey'])


@router.post(
    '/create', status_code=HTTPStatus.CREATED, response_model=APIKeySchema
)
async def create_api_key(
    api_key_service: ApiKeyService = Depends(),
    current_user: User = Depends(get_current_user),
):
    api_key = await api_key_service.generate_api_key(user=current_user)

    return api_key
