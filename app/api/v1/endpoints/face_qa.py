from http import HTTPStatus

from fastapi import APIRouter, Depends

from app.schemas.faceqa import FaceQAResponse
from app.services.faceqa_service import FaceQAService

router = APIRouter(prefix='/faceqa', tags=['FaceQA'])


@router.post('/', status_code=HTTPStatus.OK, response_model=FaceQAResponse)
async def verify_quality(
    api_key: str,
    faceqa_service: FaceQAService = Depends(),
):
    validated = await faceqa_service.validate_image(
        api_key=api_key
    )
    return validated
