from aiogram.filters import Filter
from aiogram.types import Message
from sqlalchemy import ScalarResult, select
from sqlalchemy.ext.asyncio import async_sessionmaker

from src.db.models import Auth


class Guard(Filter):
    def __init__(self, session: async_sessionmaker):
        super().__init__()
        self.session = session

    async def __call__(self, event: Message):
        async with self.session() as session:
            result: ScalarResult = await session.scalars(select(Auth).where(Auth.user_id == event.from_user.id))

            user: Auth = result.first()

            if user is None:

                return False

            if user.active is None or user.active is False:
                return False



            return True


