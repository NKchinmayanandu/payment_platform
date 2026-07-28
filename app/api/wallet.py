from app.db.session import get_db
from app.db.session import get_db
from app.schemas.token import Token
from app.schemas.user import UserCreate, UserOut
from app.services.auth_service import authenticate_user, register_user
import logging
from app.models.users import User
from app.api.dependencies import get_current_user
from fastapi import APIRouter,Depends
from app.services.wallet_service import get_user_wallet
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/wallet",tags=["/Wallet"])


@router.get("/wallet")
async def get_wallet(user_id:int,db:AsyncSession=Depends(get_db)):
    return await get_user_wallet(user_id=user_id,db=db)
