from app.models.users import User
from app.api.dependencies import get_current_user
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.services.transaction_service import transfer_money
from app.schemas.transaction import TransactionCreate, TransactionOut
from fastapi import Depends, Header
from uuid import UUID
router = APIRouter(prefix="/wallet", tags=["/Wallet"])


@router.post("/transfer", response_model=TransactionOut)
async def send_money(
    payload: TransactionCreate,
    idempotency_key: UUID = Header(..., alias="Idempotency-Key"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await transfer_money(
        phone_number=payload.receiver_phone_number,
        amount=payload.amount,
        idempotency_key=idempotency_key,
        db=db,
        current_user=current_user,
    )