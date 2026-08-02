from pydantic import BaseModel


class ActiveUserOut(BaseModel):
    username: str
    transactions: int


class UserStatsOut(BaseModel):
    total_transactions: int
    sent_transactions: int
    received_transactions: int
