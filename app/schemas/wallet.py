from pydantic import BaseModel
import uuid
from sqlalchemy.orm import Mapped

class WalletOut(BaseModel):
    id:Mapped[uuid.UUID]
    balance:int

