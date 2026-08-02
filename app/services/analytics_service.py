from sqlalchemy.ext.asyncio import AsyncSession
from app.models.users import User
from app.repository.analytics import get_most_active_users, get_user_stats
from app.schemas.analytics import ActiveUserOut, UserStatsOut
from app.core.exceptions import NotFoundError


async def most_active_users(db: AsyncSession, limit: int = 10) -> list[ActiveUserOut]:
    rows = await get_most_active_users(db=db, limit=limit)
    return [ActiveUserOut(**row) for row in rows]


async def current_user_stats(current_user: User, db: AsyncSession) -> UserStatsOut:
    if not current_user.wallet:
        raise NotFoundError(detail="Wallet not found for user")
    stats = await get_user_stats(db=db, wallet_id=current_user.wallet.id)
    return UserStatsOut(**stats)
