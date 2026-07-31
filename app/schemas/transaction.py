from pydantic import BaseModel, ConfigDict, Field
from uuid import UUID
from app.models.transaction import TransactionStatus
from datetime import datetime


class TransactionCreate(BaseModel):
    receiver_phone_number: str
    amount: int


class TransactionOut(BaseModel):
    id: UUID = Field(validation_alias="reference_id")
    sender_wallet: UUID
    receiver_wallet: UUID
    amount: int
    status: TransactionStatus
    created_at: datetime
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)
