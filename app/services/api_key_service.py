import hashlib
import hmac
import secrets
from http import HTTPStatus

from fastapi import Depends, HTTPException
from fastapi.security.api_key import APIKeyHeader

from app.models.user import User
from app.repositories.api_key import ApiKeyRepository
from app.repositories.user import UserRepository
from app.schemas.api_key import APIKeySchema

api_key_header = APIKeyHeader(name="X-API-Key")


class ApiKeyService:
    def __init__(
        self,
        api_key_repo: ApiKeyRepository = Depends(),
        user_repo: UserRepository = Depends()
    ):
        self.api_key_repo = api_key_repo
        self.user_repo = user_repo

    async def generate_api_key(self, user: User):
        api_key = secrets.token_hex(16)
        suffix = self.get_suffix(api_key)

        hashed_key = self.get_api_key_hash(api_key)

        await self.api_key_repo.create(
            hashed_key=hashed_key, suffix=suffix, user=user
        )

        return APIKeySchema(api_key=api_key)

    @staticmethod
    def get_api_key_hash(api_key: str):
        return hashlib.sha256(api_key.encode()).hexdigest()

    def verify_api_key_hash(self, api_key: str, stored_hash: str):
        provided_hash = self.get_api_key_hash(api_key)

        return hmac.compare_digest(provided_hash, stored_hash)

    @staticmethod
    def get_suffix(api_key: str):
        return api_key[-5:]

    async def validate_api_key(self, api_key: str):
        suffix = self.get_suffix(api_key)

        db_key = await self.api_key_repo.read_by_suffix(suffix)

        if not db_key:
            raise HTTPException(
                status_code=HTTPStatus.UNAUTHORIZED, detail='Invalid API key'
            )

        return db_key

    async def get_current_user_from_api_key(
        self, api_key: str = Depends(api_key_header),
    ):
        db_key = await self.validate_api_key(api_key)

        current_user = await self.user_repo.read_by_id(db_key.user_id)

        return current_user
