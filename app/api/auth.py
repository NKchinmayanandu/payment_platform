from fastapi import APIRouter,Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.models.users import User
from app.schemas.token import Token
from app.schemas.user import UserCreate, UserOut
from app.services.auth_service import authenticate_user, register_user
import logging
router = APIRouter(prefix="/auth",tags=["/Auth"])

@router.post("/register")
async def register(user_in:UserCreate,db:AsyncSession=Depends(get_db)):
    logging.info("user is being started to create")
    return register_user(user_in=user_in,db=db)