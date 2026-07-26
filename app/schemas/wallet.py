from pydantic import BaseModel
from sqlalchemy import UUID
class WalletOut(BaseModel):
    id:UUID
    balance:int

