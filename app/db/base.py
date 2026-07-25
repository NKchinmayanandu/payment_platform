from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from app.models.users import User
    from app.models.transaction import Transaction,TransactionStatus
    from app.models.wallets import Wallet
