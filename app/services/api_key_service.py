import hashlib
import hmac
import secrets
from http import HTTPStatus

from fastapi import Depends, HTTPException

from app.repositories.api_key import ApiKeyRepository


class ApiKeyService:
    def __init__(self, api_key_repo: ApiKeyRepository = Depends()):
        self.api_key_repo = api_key_repo

    @staticmethod
    def generate_api_key():
        return secrets.token_hex(16)

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

        return db_key.user
