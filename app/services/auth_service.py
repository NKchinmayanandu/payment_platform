from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import AlreadyExistsError, UnauthorizedError, NotFoundError
from app.core.security import create_access_token, hash_password, verify_password
from app.models.users import User
from app.models.wallets import Wallet
from app.schemas.token import Token
from app.schemas.user import UserCreate, UserOut
from app.repository.register import create_user_in_db,create_wallet,check_user

async def register_user(user_in:UserCreate,db:AsyncSession):
      result = await check_user(user_email=user_in.email,db=db)
      if result:
            raise AlreadyExistsError(detail="email already exists")

      try:
            hashed_pw = hash_password(user_in.password)

            user = await create_user_in_db(db, user_in, hashed_pw)

            wallet = await create_wallet(user_id=user.id,db=db)

            await db.commit()
            await db.refresh(user)
            await db.refresh(wallet)
            return UserOut.model_validate(user)

      except Exception:
            await db.rollback()
            raise

async def authenticate_user(db:AsyncSession,username:str,password:str):
      result = await check_user(user_email=username,db=db)
      if not result or not verify_password(password, result.hashed_password):
            raise UnauthorizedError(detail="Invalid password or email")
      token = create_access_token({"user_id": result.id})
      return Token(access_token=token)
      