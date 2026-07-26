from sqlalchemy.orm import Mapped,mapped_column,relationship
from app.db.base import Base
from sqlalchemy import func,Enum,UUID,ForeignKey
from datetime import datetime
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .wallets import Wallet
import enum
import uuid
class TransactionStatus(str, enum.Enum):
    QUEUED = "QUEUED"
    PENDING = "PENDING"
    FAILED = "FAILED"
    SUCCESS = "SUCCESS"

class Transaction(Base):
    __tablename__ = "transactions"
    id : Mapped[int] = mapped_column(primary_key=True)
    sender_wallet : Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True),ForeignKey("wallets.id"))
    receiver_wallet : Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True),ForeignKey("wallets.id"))
    amount : Mapped[int]
    status : Mapped[TransactionStatus] = mapped_column(
        type_=Enum(TransactionStatus, name="transactionstatus", create_type=False),
        default=TransactionStatus.QUEUED
    )
    created_at : Mapped[datetime] = mapped_column(server_default=func.now())    
    