from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from decouple import config


engine = create_engine(f'postgresql://{config("DB_USER")}:{config("DB_PASSWORD")}@127.0.0.1:5432/wsgiref_sqlalchemy', echo=True)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()
