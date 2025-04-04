from app.schemas.faceqa import FaceQARequest, FaceQAResponse
from app.services.api_key_service import ApiKeyService
from app.services.credit_service import CreditService


class FaceQAService:
    def __init__(
        self, api_key_service: ApiKeyService, credit_service: CreditService
    ):
        self.api_key_service = api_key_service
        self.credit_service = credit_service

    async def validate_image(self, request: FaceQARequest):
        user = await self.api_key_service.validate_api_key(request.api_key)

        await self.credit_service.consume_credits(user=user, amount=1)

        quality_score = 0.7  # Implementar Logica

        return FaceQAResponse(quality_score=quality_score)
