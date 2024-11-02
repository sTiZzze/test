from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from config.database import get_db
from src.domain.models.user import User
from src.domain.DTO.user import CreateUser, UserResponse
from src.applications.user import UserService
from src.infrastructure.utils.deps import get_current_user

router_auth = APIRouter()


@router_auth.post('/signup', response_model=UserResponse)
async def create_user(data: CreateUser):
    async with get_db() as session:
        service = UserService(session)
    return await service.create_user(User, data)


@router_auth.post('/login')
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    async with get_db() as session:
        service = UserService(session)
    return await service.login_user(User, form_data)


@router_auth.get('/me', response_model=UserResponse)
async def get_me(user: CreateUser = Depends(get_current_user)):
    return user