from main.views import OrganizationViewSet, ProductViewSet
from server.distributor import route


plugs = [
    route('organizations', OrganizationViewSet()),
    route('products', ProductViewSet()),
]
