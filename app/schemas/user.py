from pydantic import BaseModel, ConfigDict, EmailStr  # noqa


class UserSchema(BaseModel):
    email: EmailStr
    password: str

    model_config = ConfigDict(from_attributes=True)


class UserPublic(BaseModel):
    id: int
    email: EmailStr
    model_config = ConfigDict(from_attributes=True)


class UserList(BaseModel):
    users: list[UserPublic]


class UserUpdateMe(BaseModel):
    email: EmailStr


class UpdatePassword(BaseModel):
    current_password: str
    new_password: str
