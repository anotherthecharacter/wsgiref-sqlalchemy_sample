from abc import ABC, abstractproperty

from sqlalchemy.exc import DataError, IntegrityError

from server.utils import Session, SerializerError, SerializerErrorDetails, get_object_or_404


class ModelViewSet:

    class Meta(ABC):

        @abstractproperty
        def model():
            ...
        
        
        @abstractproperty
        def serializer():
            ...


    def list_create(self, method, data, pk):
        if method == 'GET':
            with Session() as session:
                queryset = session.query(self.Meta.model).order_by(self.Meta.model.id)
                serializer = self.Meta.serializer().represent(queryset)
    
                return ('200 OK', serializer)
        elif method == 'POST':
            with Session() as session:
                try:
                    serializer = self.Meta.serializer().validate(data)

                    if isinstance(serializer, SerializerErrorDetails):
                        error = serializer
                        raise SerializerError
                    
                    session.add(serializer)
                    session.commit()
                except SerializerError:
                    session.rollback()
                    return ('400 Bad Request', error)
                except IntegrityError:
                    session.rollback()
                    return ('404 Not Found', {'detail': 'Invalid Primary Key.'})
                except DataError:
                    session.rollback()
                    return ('400 Bad Request', {'detail': 'An Unexpected Error Occurred. Invalid Fields.'})
                else:
                    return ('201 Created', self.Meta.serializer().represent(serializer, many=False))
        else:
            return ('405 Method Not Allowed', ())


    def retrieve_update_delete(self, method, data, pk):
        if method == 'GET':
            with Session() as session:
                queryitem = get_object_or_404(self.Meta.model, pk, session)
                serializer = self.Meta.serializer().represent(queryitem)
                
                return ('200 OK', serializer)
        elif method == 'PATCH':
            with Session() as session:
                queryitem = get_object_or_404(self.Meta.model, pk, session)
                self.Meta.serializer().partial_update(queryitem, data)
                session.commit()

                return ('200 OK', self.Meta.serializer().represent(queryitem))
        elif method == 'DELETE':
            with Session() as session:
                queryitem = get_object_or_404(self.Meta.model, pk, session)[0]
                session.delete(queryitem)
                session.commit()

                return ('204 No Content', self.Meta.serializer().represent(queryitem, many=False))
        elif method == 'PUT':
            with Session() as session:
                try:
                    queryitem = get_object_or_404(self.Meta.model, pk, session)
                    serializer = self.Meta.serializer().update(queryitem, data)

                    if isinstance(serializer, SerializerErrorDetails):
                        error = serializer
                        raise SerializerError

                    session.commit()
                except SerializerError:
                    session.rollback()
                    return ('400 Bad Request', error)
                else:
                    return ('200 OK', self.Meta.serializer().represent(queryitem))
        else:
            return ('405 Method Not Allowed', ())
