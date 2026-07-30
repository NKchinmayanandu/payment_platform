from app.models.users import User
from app.api.dependencies import get_current_user
from fastapi import APIRouter,Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.services.transaction_service import transfer_money
router = APIRouter(prefix="/wallet",tags=["/Wallet"])

@router.post("/transfer")
async def send_money(phone_number:str,amount:int,
                     db:AsyncSession=Depends(get_db),
                     current_user:User=Depends(get_current_user)):
    return transfer_money(phone_number=phone_number,
                          amount=amount,db=db,
                          current_user=current_user)
