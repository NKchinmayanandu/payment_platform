from pydantic import BaseModel
import uuid
from sqlalchemy.orm import Mapped
from datetime import datetime
class WalletOut(BaseModel):
    id:uuid.UUID
    balance:int
    created_at:datetime

    model_config = {
        'from_attributes':True
    }