import enum
from typing import Optional

from sqlalchemy.engine import Engine, create_engine
from sqlalchemy import Column, Enum, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker, Session


class _SQLEngine:
    def __init__(self):
        self.engine: Optional[Engine] = None
        self.session_maker = None
        self._params = None

    def setup(self, *, host: str, port: int, user: str, password: str, database: str):
        self.engine = create_engine(
            f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}",
            pool_pre_ping=True,
        )
        self.session_maker = sessionmaker(self.engine, expire_on_commit=False)

    def _ensure_setup(self):
        if self.engine is None:
            self.setup(**self._params)

    def lazy_setup(self, **kwargs):
        self._params = kwargs

    def get_session(self) -> Session:
        self._ensure_setup()
        return self.session_maker()


DATABASE = _SQLEngine()

Base = declarative_base()


class ProductType(enum.Enum):
    CLOTHING = "clothing"
    KITCHEN = "kitchen"
    FURNITURE = "furniture"
    LIGHTING = "lighting"
    BOOKS = "books"


class Product(Base):
    __tablename__ = "product"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    type = Column(Enum(ProductType, values_callable=lambda obj: [e.value for e in obj]), nullable=False)
    price = Column(Integer, nullable=False)
