from fastapi import Depends

from app.schemas.faceqa import FaceQARequest, FaceQAResponse
from app.services.api_key_service import ApiKeyService
from app.services.credit_service import CreditService


class FaceQAService:
    def __init__(
        self,
        api_key_service: ApiKeyService = Depends(),
        credit_service: CreditService = Depends(),
    ):
        self.api_key_service = api_key_service
        self.credit_service = credit_service

    async def validate_image(self, api_key: str):
        user = await self.api_key_service.validate_api_key(api_key)     # Provavelmente aqui

        await self.credit_service.consume_credits(user=user, amount=1)

        quality_score = 0.7

        return FaceQAResponse(quality_score=quality_score)
