from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from sqlalchemy import BigInteger, String, ForeignKey, Boolean

engine = create_async_engine(url='sqlite+aiosqlite:///db.sqlite3')

async_session = async_sessionmaker(engine)

class Base(AsyncAttrs, DeclarativeBase):
    pass

class User (Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id = mapped_column(BigInteger)
    name: Mapped[str] = mapped_column(String(30))
    username: Mapped[str] = mapped_column(String(30))
    # status: Mapped[int] = mapped_column()

class Admins (Base):
    __tablename__ = 'admins'

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id = mapped_column(BigInteger)
    name: Mapped[str] = mapped_column(String(30))
    username: Mapped[str] = mapped_column(String(30))  
    status: Mapped[str] = mapped_column(String(2)) 

class Category (Base):
    __tablename__ = 'categories'

    id: Mapped[int] = mapped_column(primary_key=True)
    topic: Mapped[str] = mapped_column(String(30))

class Note (Base):
    __tablename__ = 'notes'

    id: Mapped[int] = mapped_column(primary_key=True)
    topic: Mapped[str] = mapped_column(ForeignKey('categories.id'))
    question: Mapped[str] = mapped_column(String(50))
    explanation: Mapped[str] = mapped_column(String(2000))

class Appeal (Base):
    __tablename__ = 'appeals'

    id: Mapped[int] = mapped_column(primary_key=True)
    id_user = mapped_column(BigInteger)
    question: Mapped[str] = mapped_column(String(1000))
    active: Mapped[str] = mapped_column(String(15))

class Online (Base):
    __tablename__ = 'online'

    id: Mapped[int] = mapped_column(primary_key=True)
    id_user = mapped_column(BigInteger)
    id_admin = mapped_column(BigInteger)
    active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
