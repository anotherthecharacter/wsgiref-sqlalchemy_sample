from decouple import config
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from main.models import Product
from server.utils import HTTP404, get_object_or_404


engine = create_engine(f'postgresql://{config("DB_USER")}:{config("DB_PASSWORD")}@127.0.0.1:5432/wsgiref_sqlalchemy', echo=False)
Session = sessionmaker(bind=engine)


class ProductViewSet:

    def list_create(self, method, data, pk):
        if method == 'GET':
            with Session() as session:
                response = []

                products = session.query(Product).order_by(Product.id)

                for product in products:
                    response.append({'id': product.id, 'title': product.title, 'price': float(product.price), 'quantity': product.quantity, 'description': product.description})

                return ('200 OK', response)
        elif method == 'POST':
            with Session() as session:
                try:
                    serializer = Product(title=data['title'], price=data['price'], quantity=data['quantity'], description=data.get('description'))
                    session.add(serializer)
                    session.commit()
                except:
                    session.rollback()
                    return ('400 Bad Request', ())
                else:
                    return ('201 Created', ({'id': serializer.id, 'title': serializer.title, 'price': float(serializer.price), 'quantity': serializer.quantity, 'description': serializer.description}))
        else:
            return ('405 Method Not Allowed', ())


    def retrieve_update_delete(self, method, data, pk):
        if method == 'GET':
            with Session() as session:
                response = []

                product = get_object_or_404(Product, pk, session)[0]
                response.append({'id': product.id, 'title': product.title, 'price': float(product.price), 'quantity': product.quantity, 'description': product.description})
                
                return ('200 OK', response)
        elif method == 'PUT':
            with Session() as session:
                try:
                    product = get_object_or_404(Product, pk, session)

                    session.query(Product).update({Product.title: data['title'], Product.price: data['price'], Product.quantity: data['quantity'], Product.description: data.get('description')})
                    session.commit()
                except:
                    session.rollback()
                    return ('400 Bad Request', ())
                else:
                    return ('200 OK', ())
        elif method == 'PATCH':
            with Session() as session:
                try:
                    product = get_object_or_404(Product, pk, session)
                    
                    product.update({Product.title: data['title'], Product.price: data['price'], Product.quantity: data['quantity'], Product.description: data.get('description')})
                    session.commit()
                except:
                    session.rollback()
                    return ('400 Bad Request', ())
                else:
                    return ('200 OK', ())
        elif method == 'DELETE':
            with Session() as session:
                product = get_object_or_404(Product, pk, session)[0]

                session.delete(product)
                session.commit()

                return ('204 No Content', ())
        else:
            return ('405 Method Not Allowed', ())
