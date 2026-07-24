from sqlalchemy.orm import Mapped,mapped_column,relationship
from app.db.base import Base
from sqlalchemy import String,func,ForeignKey,Enum
from datetime import datetime
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .wallets import Wallet
import enum

class TransactionStatus(str, enum.Enum):
    QUEUED = "QUEUED"
    DEPLOYING = "DEPLOYING"
    RUNNING = "RUNNING"
    STOPPED = "STOPPED"
    FAILED = "FAILED"
    RESTARTING = "RESTARTING"
    STARTING = "STARTING"
    REMOVED = "REMOVED"

class Transaction(Base):
    __tablename__ = "transactions"
    id : Mapped[int] = mapped_column(primary_key=True)
    sender_wallet : Mapped[int] = mapped_column(ForeignKey="wallets.id")
    receiver_wallet : Mapped[int] = mapped_column(ForeignKey="wallets.id")
    amount : Mapped[int]
    status : Mapped[TransactionStatus] = mapped_column(
        type_=Enum(TransactionStatus, name="transactionstatus", create_type=False),
        default=TransactionStatus.QUEUED
    )
    created_at : Mapped[datetime] = mapped_column(server_default=func.now())