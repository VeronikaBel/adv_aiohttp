import os
import datetime
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, DateTime, func, Text

POSTGRES_USER = os.getenv('POSTGRES_USER', 'postgres') 
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD', '821311')
POSTGRES_HOST = os.getenv('POSTGRES_HOST', '127.0.0.1')
POSTGRES_PORT = os.getenv('POSTGRES_PORT', '5431')
POSTGRES_DB = os.getenv('POSTGRES_DB', 'adv_aiohttp')


PG_DSN = (                     # это строчка подключения к БД
    f"postgresql+asyncpg://"   # asyncpg - библиотека,которая является драйвером,иначе alchemy будет пытаться использовать psycopg2
    f"{POSTGRES_USER}:{POSTGRES_PASSWORD}@"
    f"{POSTGRES_HOST}:{POSTGRES_PORT}/" 
    f"{POSTGRES_DB}"
)

engine = create_async_engine(PG_DSN) #подключение к базе

Session = async_sessionmaker(bind=engine, expire_on_commit=False) # создаём фабрику сессий + импорт async_sessionmaker
                                         # expire_on_commit - чтобы сессия не закрывалась после каждого коммита


class Base(DeclarativeBase, AsyncAttrs):
    @property
    def id_dict(self):
        return {"id": "self.id"}

class Advertisement(Base):
    __tablename__ = "adv"

    id: Mapped[int] = mapped_column(Integer, primary_key= True)
    title: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=func.now())
    owner_id: Mapped[int] = mapped_column(Integer, nullable=False)

@property #задаём свойство преобразования в словарик
def dict(self):
    return {
        "id": self.id,
        "title": self.title,
        "description": self.description,
        "created_at": int(self.created_at.timestamp()), #timestamp - с плавающей точкой - мы преобразуем его в число
        "owner_id": self.owner_id
    }
    
async def init_orm():  #создаёт таблицу в "асинхроне" (инициализирует схемы)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all) 
        
async def close_orm():  #закрытие сессии создания таблицы=Отключение от базы=закрывает ORM
    await engine.dispose()