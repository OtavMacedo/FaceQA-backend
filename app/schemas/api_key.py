from pydantic import BaseModel


class APIKeySchema(BaseModel):
    api_key: str
    id: int
