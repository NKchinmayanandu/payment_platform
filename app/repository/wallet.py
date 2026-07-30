from sqlalchemy.ext.asyncio import AsyncSession
from app.models.users import User
from app.models.wallets import Wallet
from sqlalchemy import select
from app.core.exceptions import NotFoundError
import logging

async def get_wallet_db(user_id:int,db:AsyncSession):
    result = await db.execute(select(Wallet).where(Wallet.owner_id == user_id))
    result = result.scalar_one_or_none()
    if result is None:
        logging.error("wallet not found check immediately!!")
        raise NotFoundError(detail="wallet not found")
    return result

async def update_wallet_db(user_id: int, db: AsyncSession) -> Wallet:
    stmt = (
        select(Wallet)
        .where(Wallet.owner_id == user_id)
        .with_for_update()
    )

    result = await db.execute(stmt)
    wallet = result.scalar_one()

    return wallet
