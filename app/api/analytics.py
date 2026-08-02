from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_current_user
from app.db.session import get_db
from app.models.users import User
from app.schemas.analytics import ActiveUserOut, UserStatsOut
from app.services.analytics_service import most_active_users, current_user_stats

router = APIRouter(tags=["Analytics"])


@router.get(
    "/analytics/most-active-users",
    response_model=list[ActiveUserOut],
    summary="Top 10 most active users by transaction count",
)
async def top_active_users(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Returns the top 10 users ranked by total number of transactions
    (sent + received). No financial data is exposed.
    """
    return await most_active_users(db=db)


@router.get(
    "/me/stats",
    response_model=UserStatsOut,
    summary="Current user's transaction statistics",
)
async def my_stats(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Returns the authenticated user's own transaction summary:
    total, sent, and received counts.
    """
    return await current_user_stats(current_user=current_user, db=db)
