from fastapi import APIRouter,Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.schemas.token import Token
from app.schemas.user import UserCreate, UserOut
from app.services.auth_service import authenticate_user, register_user
import logging
from app.models.users import User
from app.api.dependencies import get_current_user
router = APIRouter(prefix="/auth",tags=["/Auth"])

@router.post("/register")
async def register(user_in:UserCreate,db:AsyncSession=Depends(get_db)):
    logging.info("user is being started to create")
    return await register_user(user_in=user_in,db=db) 

@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db),
):
    return await authenticate_user(db, form_data.username, form_data.password)


@router.get("/me", response_model=UserOut)
async def me(current_user: User = Depends(get_current_user)):
    return UserOut.model_validate(current_user)