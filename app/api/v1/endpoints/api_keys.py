from http import HTTPStatus

from fastapi import APIRouter, Depends

from app.core.security import get_current_user
from app.models.user import User
from app.repositories.api_key import APIKeyRepository
from app.schemas.api_key import APIKeySchema
from app.services.api_key_service import generate_api_key

router = APIRouter(prefix='/api-keys', tags=['APIKey'])


@router.post(
    '/create', status_code=HTTPStatus.CREATED, response_model=APIKeySchema
)
async def create_api_key(
    api_key_repository: APIKeyRepository = Depends(APIKeyRepository),
    current_user: User = Depends(get_current_user),
):
    api_key = generate_api_key()
    api_suffix = api_key[-5:]

    db_api_key = await api_key_repository.create(
        api_key=api_key, user=current_user, suffix=api_suffix
    )
    return APIKeySchema(api_key=api_key, id=db_api_key.id)
