from abc import ABC, abstractproperty

from server.utils import SerializerErrorDetails


class ModelSerializer:

    class Meta(ABC):

        @abstractproperty
        def model(self):
            ...
        

        @abstractproperty
        def immutable_fields(self):
            ... 
        
        
        @abstractproperty
        def required_fields(self):
            ...        
        

        @abstractproperty
        def optional_fields(self):
            ...


    def validate(self, data):
        error = SerializerErrorDetails()
        result = {}

        for field in self.Meta.required_fields:
            key = field[0]

            if not data.get(key):
                error.update({key: 'This field is required.'})
            
            result.update({key: data.get(key)})
        
        for field in self.Meta.optional_fields:
            key = field[0]

            if not data.get(key):
                continue    
        
            result.update({key: data.get(key)})
        
        if error:
            return error
        
        return self.Meta.model(**result)


    def update(self, obj, data):
        error = SerializerErrorDetails()
        result = {}

        for field in self.Meta.required_fields:
            key = field[0]

            if not data.get(key):
                error.update({key: 'This field is required.'})

            result.update({eval(f'{self.Meta.model.__name__}.{key}'): data.get(key)})

        for field in self.Meta.optional_fields:
            key = field[0]

            if not data.get(key):
                continue    
            
            result.update({eval(f'{self.Meta.model.__name__}.{key}'): data.get(key)})

        if error:
            return error
        
        return obj.update(result)


    def partial_update(self, obj, data):
        result = {}

        for field in (self.Meta.required_fields + self.Meta.optional_fields):
            key = field[0]

            if not data.get(key):
                continue

            result.update({eval(f'{self.Meta.model.__name__}.{key}'): data.get(key)})
        
        if result:
            return obj.update(result)


    def to_representation(self, obj):
        result = {}

        for field in (self.Meta.immutable_fields + self.Meta.required_fields + self.Meta.optional_fields):
            key = field[0]
            datatype = field[1]
            value = datatype(eval(f'obj.{key}'))

            result.update({key: value})
        
        return result


    def represent(self, query, many=True):
        if many == True:
            result = []

            for obj in query:
                result.append(self.to_representation(obj))
            
            return result
        
        return self.to_representation(query)
