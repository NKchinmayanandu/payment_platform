from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import AlreadyExistsError, UnauthorizedError
from app.core.security import create_access_token, hash_password, verify_password
from app.models.users import User
from app.models.wallets import Wallet
from app.schemas.token import Token
from app.schemas.user import UserCreate, UserOut
from app.repository.register import create_user_in_db,create_wallet


async def register_user(user_in:UserCreate,db:AsyncSession):
      result = await db.execute(select(User).where(User.email == user_in.email))
      if result.scalar_one_or_none():
            raise AlreadyExistsError(detail="email already exists")

      try:
            hashed_pw = hash_password(user_in.password)

            user = await create_user_in_db(db, user_in, hashed_pw)

            wallet = await create_wallet(db, user.id)

            await db.commit()
            await db.refresh(user)
            await db.refresh(wallet)
            return result

      except Exception:
            await db.rollback()
            raise

    