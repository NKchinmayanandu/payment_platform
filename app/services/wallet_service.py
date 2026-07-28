from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.wallet import WalletOut
from app.repository.register import create_user_in_db,create_wallet,check_user
from app.repository.wallet import get_wallet_db
async def get_user_wallet(user_id:int,db:AsyncSession):
    result = await get_wallet_db(user_id=user_id,db=db)
    return WalletOut.model_validate(result)