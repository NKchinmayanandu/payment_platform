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
from app.services.wallet_service import add_deposit_user
router = APIRouter(prefix="/wallet",tags=["/Wallet"])


@router.get("")
async def get_wallet(current_user:User=Depends(get_current_user),db:AsyncSession=Depends(get_db)):
    return await get_user_wallet(user_id=current_user.id,db=db)

@router.post("/deposit")
async def add_balance(add_deposit:int,current_user:User=Depends(get_current_user),db:AsyncSession=Depends(get_db)):
    return await add_deposit_user(deposit=add_deposit,current_user=current_user,db=db)

