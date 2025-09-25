from sqlalchemy import Column, BigInteger, Text, Boolean

from src.db.database import Base


class Auth(Base):
    __tablename__ = 'tg_auth'
    id = Column(BigInteger, unique=True, primary_key=True, autoincrement=True)

    user_id = Column(BigInteger, unique=True)
    username = Column(Text, unique=True, nullable=True)
    # email = Column(Text, unique=False, nullable=False)
    active = Column(Boolean, unique=False, nullable=True, default=True, insert_default=False)



    def __str__(self) -> str:
        return f"<USER: {self.user_id, self.username, self.active}>"