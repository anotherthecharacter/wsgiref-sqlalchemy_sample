from decouple import config
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from main.models import Product


engine = create_engine(f'postgresql://{config("DB_USER")}:{config("DB_PASSWORD")}@127.0.0.1:5432/wsgiref_sqlalchemy', echo=False)
session = sessionmaker(bind=engine)()


class ProductViewSet:

    def list_create(self, method, data):
        if method == 'GET':
            response = []
            products = session.query(Product).all()
            for product in products:
                response.append({'title': product.title, 'price': product.price, 'quantity': product.quantity, 'description': product.description})

            return response
        elif method == 'POST':
            try:
                serializer = Product(title=data['title'], price=data['price'], quantity=data['quantity'], description=data.get('description'))
                session.add(serializer)
                session.commit()
            except:
                print('Except block')

            return 'OK'
        else:
            return 405


    def retrieve_update_delete(self, method, data):
        if method == 'GET':
            ...
        elif method == 'PUT':
            print('retrieve_update_delete')
            print('method', method)
            print('data', data)
        elif method == 'PATCH':
            ...
        elif method == 'DELETE':
            ...
        else:
            return 405
