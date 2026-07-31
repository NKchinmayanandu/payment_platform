from sqlalchemy.orm import Mapped,mapped_column,relationship
from app.db.base import Base
from sqlalchemy import func,UUID,ForeignKey,String,JSON,UniqueConstraint
from datetime import datetime
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .users import User
import uuid
class IdempotencyKey(Base):
    __tablename__ = "idempotency_keys"

    id = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    key = mapped_column(UUID(as_uuid=True), nullable=False, index=True)

    user_id = mapped_column(ForeignKey("users.id"), nullable=False)

    endpoint = mapped_column(String, nullable=False)

    response = mapped_column(JSON)
    
    created_at : Mapped[datetime] = mapped_column(server_default=func.now())    

    __table_args__ = (UniqueConstraint("user_id", "key"),)