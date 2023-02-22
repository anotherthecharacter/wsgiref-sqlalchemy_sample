class ProductViewSet:

    def list_create(self):
        return [{"title": "milk", "price": 888}, {"title": "bread", "price": 100}]


    def retrieve_update_delete(self):
        print('retrieve_update_delete')
