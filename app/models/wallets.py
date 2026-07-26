from sqlalchemy.orm import Mapped,mapped_column,relationship
from app.db.base import Base
from sqlalchemy import func,ForeignKey
from datetime import datetime
from sqlalchemy import UUID
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .users import User
    from .transaction import Transaction
import uuid
class Wallet(Base):
    __tablename__="wallets"
    id: Mapped[uuid.UUID] = mapped_column(
            UUID(as_uuid=True), primary_key=True, 
            default=uuid.uuid4
            )
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE",unique=True))
    balance : Mapped[int] 
    owner: Mapped["User"] = relationship(back_populates="wallet")

    created_at : Mapped[datetime] = mapped_column(server_default=func.now())

    sent_transactions: Mapped[list["Transaction"]] = relationship(
        back_populates="sender", foreign_keys="[Transaction.sender_wallet]"
        )

    received_transactions: Mapped[list["Transaction"]] = relationship(
        back_populates="receiver", foreign_keys="[Transaction.receiver_wallet]"
        )