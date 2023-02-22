from main.views import ProductViewSet
from server.distributor import route


plugs = [
    route('products', ProductViewSet()),
]
