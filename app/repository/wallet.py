from sqlalchemy.ext.asyncio import AsyncSession
from app.models.users import User
from app.models.wallets import Wallet
from sqlalchemy import select

async def get_wallet_db(user_id:int,db:AsyncSession):
    result = await db.execute(select(Wallet).where(Wallet.owner_id == user_id))
    result = result.scalar_one_or_none()
    return result
