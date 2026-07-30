from app.models.users import User
from sqlalchemy.ext.asyncio import AsyncSession
from app.repository.user_transaction import get_user_phone,get_user_wallet_transfer
import logging
from app.repository.wallet import update_wallet_db
from app.models.transaction import Transaction,TransactionStatus
from app.core.exceptions import ForbiddenError,NotFoundError
from app.schemas.transaction import TransactionOut
async def transfer_money(phone_number:str,amount:int,
                     db:AsyncSession,
                     current_user:User):
    

    user2  = await get_user_phone(phone_number=phone_number,
                          db=db)

    wallets = await get_user_wallet_transfer(user_id1=current_user.id,user_id2=user2.id,
                                       db=db)
    if len(wallets) != 2:
        raise NotFoundError(detail="the wallet u want to send dont exists")
    wallet1 = wallets[0]
    wallet2 = wallets[1]
    if wallet1.owner_id == current_user.id:
        sender = wallet1
        receiver = wallet2
    else:
        sender = wallet2
        receiver = wallet1
    if amount <= 0:
        raise ForbiddenError(detail="u cannot deposit negative money!")
    elif amount > sender.balance:
        raise ForbiddenError(detail="u dont have sufficent balance for the transaction")
    elif sender.id == receiver.id:
        raise ForbiddenError(detail="u are not supposed to transfer urself")
    
    sender.balance -= amount
    receiver.balance += amount

    transaction = Transaction(
        sender_wallet = wallet1.id,
        receiver_wallet = wallet2.id,
        amount = amount,
        status = TransactionStatus.SUCCESS,

    )
    db.add(transaction)
    try:
        await db.commit()
        await db.refresh(transaction)
    except Exception:
        logging.error("commiting to db failed")
        await db.rollback()
    return TransactionOut.model_validate(transaction)
