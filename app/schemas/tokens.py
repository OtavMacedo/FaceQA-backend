from pydantic import BaseModel


class LoginToken(BaseModel):
    access_token: str
    access_token_type: str
    refresh_token: str
