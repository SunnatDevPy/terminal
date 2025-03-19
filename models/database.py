from _ctypes_test import func
from datetime import datetime

from sqlalchemy import BigInteger, delete as sqlalchemy_delete, DateTime, update as sqlalchemy_update, func, desc
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, AsyncAttrs
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.future import select
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Mapped, mapped_column, selectinload

from config import conf


class Base(AsyncAttrs, DeclarativeBase):

    @declared_attr
    def __tablename__(self) -> str:
        __name = self.__name__[:1]
        for i in self.__name__[1:]:
            if i.isupper():
                __name += '_'
            __name += i
        __name = __name.lower()

        if __name.endswith('y'):
            __name = __name[:-1] + 'ie'
        return __name + 's'


class AsyncDatabaseSession:
    def __init__(self):
        self._session = None
        self._engine = None

    def __getattr__(self, name):
        return getattr(self._session, name)

    def init(self):
        self._engine = create_async_engine(conf.db.db_url)
        self._session = sessionmaker(self._engine, expire_on_commit=False, class_=AsyncSession)()

    async def create_all(self):
        async with self._engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async def drop_all(self):
        async with self._engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)


db = AsyncDatabaseSession()
db.init()


# ----------------------------- ABSTRACTS ----------------------------------
class AbstractClass:
    @staticmethod
    async def commit():
        try:
            await db.commit()
        except Exception as e:
            print(e)
            await db.rollback()

    @classmethod
    async def create(cls, **kwargs):  # Create
        object_ = cls(**kwargs)
        db.add(object_)
        await cls.commit()
        return object_

    @classmethod
    async def update(cls, id_, **kwargs):
        query = (
            sqlalchemy_update(cls)
            .where(cls.id == id_)
            .values(**kwargs)
            .execution_options(synchronize_session="fetch")
        )
        await db.execute(query)
        await cls.commit()

    @classmethod
    async def get(cls, _id, *, relationship=None):
        query = select(cls).where(cls.id == _id)
        if relationship:
            query = query.options(selectinload(relationship))
        return (await db.execute(query)).scalar()

    @classmethod
    async def get_from_username_and_password(cls, password, user_name, *, relationship=None):
        query = select(cls).where(cls.password == password, cls.username == user_name)
        if relationship:
            query = query.options(selectinload(relationship))
        return (await db.execute(query)).scalar()

    @classmethod
    async def from_user(cls, _id, *, relationship=None):
        query = select(cls).where(cls.bot_user_id == _id).order_by(desc(cls.id))
        if relationship:
            query = query.options(selectinload(relationship))
        return (await db.execute(query)).scalars()

    @classmethod
    async def from_user_order(cls, _id, *, relationship=None):
        query = select(cls).where(cls.user_id == _id).order_by(desc(cls.id))
        if relationship:
            query = query.options(selectinload(relationship))
        return (await db.execute(query)).scalar()

    @classmethod
    async def count(cls):
        query = select(func.count()).select_from(cls)
        return (await db.execute(query)).scalar()

    @classmethod
    async def delete(cls, id_):
        query = sqlalchemy_delete(cls).where(cls.id == id_)
        await db.execute(query)
        await cls.commit()

    @classmethod
    async def filter(cls, criteria, *, relationship=None, columns=None):
        if columns:
            query = select(*columns)
        else:
            query = select(cls)

        query = query.where(criteria)

        if relationship:
            query = query.options(selectinload(relationship))
        return (await db.execute(query)).scalars().all()

    @classmethod
    async def all(cls):
        return (await db.execute(select(cls))).scalars().all()

    @classmethod
    async def get_cart_from_shop(cls, user_id, shop_id):
        return (await db.execute(select(cls).where(cls.bot_user_id == user_id, cls.shop_id == shop_id))).scalars().all()

    @classmethod
    async def from_shop(cls, shop_id):
        return (await db.execute(select(cls).where(cls.shop_id == shop_id))).scalars().all()

    @classmethod
    async def get_cart_from_product(cls, user_id, product_id):
        return (await db.execute(select(cls).where(cls.bot_user_id == user_id, cls.product_id == product_id))).scalar()

    @classmethod
    async def get_cart_from_user(cls, user_id):
        return (await db.execute(select(cls).where(cls.bot_user_id == user_id))).scalars().all()

    @classmethod
    async def get_order_items(cls, order_id):
        return (await db.execute(select(cls).where(cls.order_id == order_id))).scalars().all()

    @classmethod
    async def get_from_name(cls, address):
        return (await db.execute(select(cls).where(cls.address == address))).scalars().all()

    @classmethod
    async def search_shops(cls, name, category_id=None):
        if category_id:
            return (await db.execute(
                select(cls).where(cls.category_id == category_id, cls.name.ilike(f"%{name}%")))).scalars().all()
        else:
            return (await db.execute(select(cls).filter(cls.name.ilike(f"%{name}%")))).scalars().all()

    # def run_async(self, func, *args, **kwargs):
    #     return asyncio.run(func(*args, **kwargs))

    # def convert_uzs(self, amount: int):
    #     return amount * current_price
    #
    # def convert_usd(self, amount: int):
    #     return amount // current_price


class BaseModel(Base, AbstractClass):
    __abstract__ = True
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)

    def __str__(self):
        return f"{self.id}"


class CreatedBaseModel(BaseModel):
    __abstract__ = True
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), server_onupdate=func.now())
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
