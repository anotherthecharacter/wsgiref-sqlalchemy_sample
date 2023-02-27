from decouple import config
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


Base = declarative_base()


def makemigrations():
    engine = create_engine(f'postgresql://{config("DB_USER")}:{config("DB_PASSWORD")}@127.0.0.1:5432/wsgiref_sqlalchemy', echo=True)
    Base.metadata.create_all(engine)


engine = create_engine(f'postgresql://{config("DB_USER")}:{config("DB_PASSWORD")}@127.0.0.1:5432/wsgiref_sqlalchemy', echo=False)
Session = sessionmaker(bind=engine)


class RoutingError(Exception):

    def __str__(self) -> str:
        return 'An error occurred while routing the URLs. Perhaps you have inserted a slashes "/" into suffixes?'


class HTTP404(Exception):
    pass


class SerializerError(Exception):
    pass


class SerializerErrorDetails(dict):
    pass


def get_object_or_404(model, pk, session):
    try:
        session.query(model).filter(model.id==pk)[0]
    except IndexError:
        raise HTTP404
    else:
        return session.query(model).filter(model.id==pk)
