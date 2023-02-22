from sqlalchemy import Column, Integer, String, Float, Text

from config.settings import Base, engine


class Product(Base):
    __tablename__ = 'product'

    id = Column(Integer, primary_key=True)
    title = Column(String(24))
    price = Column(Float(2))
    quantity = Column(Integer)
    description = Column(Text)


def makemigrations():    
    Base.metadata.create_all(engine)
