from pydantic import BaseModel
from sqlalchemy import UUID
from app.models.transaction import TransactionStatus
from datetime import datetime


class TransactionCreate(BaseModel):
    receiver_phone_number:int
    amount: int


class TransactionOut(BaseModel):
    id: UUID
    amount: int
    status: TransactionStatus
    sender_phone_number: str
    receiver_phone_number: str
    created_at: datetime