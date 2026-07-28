from app.models.users import User
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.wallet import WalletOut
from app.repository.wallet import get_wallet_db,update_wallet_db
from app.core.exceptions import NotFoundError,ForbiddenError
async def get_user_wallet(user_id:int,db:AsyncSession):
    result = await get_wallet_db(user_id=user_id,db=db)
    return WalletOut.model_validate(result)

async def add_deposit_user(deposit:int,current_user:User,db:AsyncSession):
    wallet = await update_wallet_db(user_id=current_user.id,db=db)
    
    if deposit <= 0:
        raise ForbiddenError(detail="u cannot deposit negative money!")
    wallet.balance += deposit   
    await db.commit()
    await db.refresh(wallet)
    return WalletOut.model_validate(wallet)
