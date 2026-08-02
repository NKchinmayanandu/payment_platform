from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, or_
from app.models.users import User
from app.models.wallets import Wallet
from app.models.transaction import Transaction


async def get_most_active_users(db: AsyncSession, limit: int = 10) -> list[dict]:
    stmt = (
        select(
            User.username,
            func.count(Transaction.id).label("transaction_count"),

        )
        .join(Wallet, Wallet.owner_id == User.id)
        .join(
            Transaction,
            or_(
                Transaction.sender_wallet == Wallet.id,
                Transaction.receiver_wallet == Wallet.id,
            ),
        )
        .group_by(User.username)
        .order_by(func.count(Transaction.id).desc())
        .limit(limit)
    )

    result = await db.execute(stmt)
    rows = result.all()
    return [{"username": row.username, "transactions": row.transaction_count} for row in rows]


async def get_user_stats(db: AsyncSession, wallet_id) -> dict:
    stmt = (
        select(
            func.count(Transaction.id)
            .filter(Transaction.sender_wallet == wallet_id)
            .label("sent"),
            func.count(Transaction.id)
            .filter(Transaction.receiver_wallet == wallet_id)
            .label("received"),
        )
        .where(
            or_(
                Transaction.sender_wallet == wallet_id,
                Transaction.receiver_wallet == wallet_id,
            )
        )
    )

    result = await db.execute(stmt)
    row = result.one()
    sent = row.sent
    received = row.received
    return {
        "total_transactions": sent + received,
        "sent_transactions": sent,
        "received_transactions": received,
    }
