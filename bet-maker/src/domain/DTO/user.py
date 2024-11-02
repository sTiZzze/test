from pydantic import BaseModel, constr


class UserBase(BaseModel):
    username: str

    class Config:
        from_attributes = True


class CreateUser(UserBase):
    password: constr(min_length=8)


class LoginUser(BaseModel):
    username: str
    password: constr(min_length=8)


class UserResponse(UserBase):
    id: int


class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str


class TokenPayload(BaseModel):
    sub: str = None
    exp: int = None