from sqlalchemy.orm import Mapped,mapped_column,relationship
from app.db.base import Base
from sqlalchemy import String,func
from datetime import datetime
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .wallets import Wallet
class User(Base):
    __tablename__="users"
    id : Mapped[int] = mapped_column(primary_key=True)
    username : Mapped[str]
    email : Mapped[str] = mapped_column(unique=True)
    hashed_password : Mapped[str] = mapped_column(String(255))
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    phone_number : Mapped[int] = mapped_column(unique=True)
    wallets : Mapped[list["Wallet"]] = relationship(
        back_populates="owner",cascade="all, delete-orphan"
    )