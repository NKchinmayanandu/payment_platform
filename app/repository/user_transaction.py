from sqlalchemy.ext.asyncio import AsyncSession
from app.models.users import User
from app.models.wallets import Wallet
from sqlalchemy import select
from app.schemas.user import UserCreate
from app.core.exceptions import NotFoundError
import logging 

async def get_user_phone(phone_number:str,db:AsyncSession):
    user = await db.execute(select(User).where(User.phone_number==phone_number))
    user = user.scalar_one_or_none()
    if not user:
        raise NotFoundError(detail="phone number doesnt exists")
    return user

async def get_user_wallet_transfer(user_id1:int,user_id2:int,db:AsyncSession):
    stmt = (
    select(Wallet)
    .where(Wallet.owner_id.in_([user_id1, user_id2]))
    .order_by(Wallet.id)
    .with_for_update()
    )
    wallets = await db.execute(stmt)
    wallets = wallets.scalars().all()
    return wallets