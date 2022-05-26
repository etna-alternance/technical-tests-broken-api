from typing import List, Optional

from fastapi import FastAPI
from fastapi.exceptions import HTTPException
from sqlalchemy import and_, select
from sqlalchemy.exc import NoResultFound

from .config import get_config

from .db import DATABASE, Product as ProductSchema, ProductType
from .models import Product, ProductCreate

app = FastAPI(
    title="broken-api",
    version="1.0.0",
)


@app.post("/product", status_code=201)
def create_product(product: ProductCreate) -> Product:
    with DATABASE.get_session() as session:
        p = ProductSchema(name=product.name, type=product.type, price=product.price)
        session.add(p)
        session.commit()
        session.refresh(p)
        return Product(id=p.id, name=p.name, type=p.type, price=p.price)


@app.get("/product/{id}")
def get_product(id: int) -> Product:
    with DATABASE.get_session() as session:
        try:
            p = session.query(ProductSchema).filter_by(id=id).first()
            return Product(id=p.id, name=p.name, type=p.type, price=p.price)
        except NoResultFound:
            raise HTTPException(status_code=404, detail=f"cannot find product with ID {id}")


@app.delete("/product/{id}")
def delete_product(id: int) -> None:
    with DATABASE.get_session() as session:
        try:
            session.query(ProductSchema).filter_by(id=id).delete()
            session.commit()
            return
        except NoResultFound:
            raise HTTPException(status_code=404, detail=f"cannot find product with ID {id}")


def build_conditions(type: Optional[ProductType], cheaper_than: Optional[int] = None):
    conditions = []
    if type is not None:
        conditions.append(ProductSchema.type == type)
    if cheaper_than is not None:
        conditions.append(ProductSchema.price < cheaper_than)
    return conditions


@app.get("/products")
def list_products(type: Optional[ProductType] = None, cheaper_than: Optional[int] = None) -> List[Product]:
    with DATABASE.get_session() as session:
        if type is None and cheaper_than is None:
            stmt = select(ProductSchema)
        else:
            stmt = select(ProductSchema).where(and_(*build_conditions(type, cheaper_than)))
        print(stmt)
        ps = session.execute(stmt).scalars().all()
        return [Product(id=p.id, name=p.name, type=p.type, price=p.price) for p in ps]


@app.on_event("startup")
def setup_database_engine():
    config = get_config().database
    DATABASE.lazy_setup(
        host=config.host,
        port=config.port,
        user=config.user,
        password=config.password,
        database=config.name,
    )
