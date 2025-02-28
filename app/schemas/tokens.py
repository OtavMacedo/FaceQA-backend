from pydantic import BaseModel


class LoginToken(BaseModel):
    access_token: str
    token_type: str
