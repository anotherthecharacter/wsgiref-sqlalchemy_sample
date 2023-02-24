from decouple import config
from sqlalchemy import Column, Integer, String, Numeric, Text
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Product(Base):
    __tablename__ = 'product'

    id = Column(Integer, primary_key=True)
    title = Column(String(24))
    price = Column(Numeric(precision=10, scale=2))
    quantity = Column(Integer)
    description = Column(Text, nullable=True)


def makemigrations():
    engine = create_engine(f'postgresql://{config("DB_USER")}:{config("DB_PASSWORD")}@127.0.0.1:5432/wsgiref_sqlalchemy', echo=True)
    Base.metadata.create_all(engine)
