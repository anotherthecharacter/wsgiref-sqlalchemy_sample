import enum

from sqlalchemy import Column, Enum, ForeignKey, Integer, Numeric, String, Text 

from server.utils import Base


class Category(enum.Enum):
    food = 'Еда'
    merchandise = 'Товары'
    other = 'Другое'


class Organization(Base):
    __tablename__ = 'organization'

    id = Column(Integer, primary_key=True)
    title = Column(String(24))
    address = Column(String(32))
    category = Column(Enum(Category))


class Product(Base):
    __tablename__ = 'product'

    id = Column(Integer, primary_key=True)
    title = Column(String(24))
    price = Column(Numeric(precision=10, scale=2))
    quantity = Column(Integer)
    description = Column(Text, default='...')
    organization = Column(ForeignKey('organization.id', ondelete='CASCADE'))
