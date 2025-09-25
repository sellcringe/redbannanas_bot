from typing import Callable, Dict, Any, Awaitable
from sqlalchemy import select, ScalarResult, update, or_
from aiogram import BaseMiddleware
from aiogram.types import Message, TelegramObject
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.db.models import Auth

## мидлварь проверяет пользователя на налицие информации в бд о нем, если нет то записываем, если да, то ничего не происходит
class RegisterCheck(BaseMiddleware):
    def __init__(self, session_pool: async_sessionmaker):
        super().__init__()
        self.session_pool = session_pool

    async def __call__(
        self,

        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable],
        event:TelegramObject,
        data: Dict[str, Any]
        ) -> Any:



        # session_maker: sessionmaker = data['sessionmaker']
        async with self.session_pool() as session:
            async with session.begin():

                # user_id = event.
                result: ScalarResult = await session.scalars(select(Auth).where(
                    or_(Auth.user_id == event.from_user.id,
                        Auth.username == event.from_user.username)

                )
                )


                user: Auth = result.one_or_none()
                if user is not None:
                    pass

                else:

                    user = Auth(
                        user_id=event.from_user.id,
                        username=event.from_user.username,
                        active=False
                    )
                    await session.merge(user)
                    await session.commit()
                if user.user_id is None:
                    await session.execute(update(Auth).where(Auth.username == event.from_user.username).values(
                        user_id=event.from_user.id, active=True))
                    await session.commit()
                        # await event.answer(f"Пользователь с логином {event.from_user.username} авторизован")
        return await handler(event,data)