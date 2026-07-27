from sqlalchemy.ext.asyncio import AsyncSession
from app.models.users import User
from app.models.wallets import Wallet
from sqlalchemy import select
from app.core.exceptions import AlreadyExistsError
from app.schemas.user import UserCreate
import logging
async def create_user_in_db(db: AsyncSession, user_in: UserCreate, hashed_password: str):
    user = User(
        username=user_in.username,
        email=user_in.email,
        hashed_password=hashed_password,
        phone_number=user_in.phone_number
    )
    db.add(user)
    await db.flush() 
    return user

async def create_wallet(user_id:int,db:AsyncSession):
    wallet_exist = await db.execute(select(Wallet).where(Wallet.owner_id==user_id))
    wallet_exist = wallet_exist.scalar_one_or_none()
    if wallet_exist:
        raise AlreadyExistsError(detail="wallet already exists")
    wallet = Wallet(
        owner_id = user_id,
        balance = 0
    )
    db.add(wallet)
    return wallet
    
async def check_user(user_email:str,db:AsyncSession):
    result = await db.execute(select(User).where(User.email==user_email))
    result = result.scalar_one_or_none()
    return result