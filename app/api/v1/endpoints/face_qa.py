from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException

from app.repositories.api_key import APIKeyRepository

router = APIRouter(prefix='/faceqa', tags=['FaceQA'])


@router.post('/', status_code=HTTPStatus.OK)
async def verify_quality(
    api_key: str,
    face_image: str,
    api_key_repository: APIKeyRepository = Depends(APIKeyRepository),
):
    api_suffix = api_key[-5:]
    db_key = await api_key_repository.read_by_suffix(api_suffix)

    if not db_key:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED, detail='Invalid API key'
        )
    key_owner = db_key.user

    if key_owner.api_credits < 1:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN, detail='Insufficient API credits'
        )
    pass
