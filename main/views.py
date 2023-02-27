from main.models import Organization, Product
from main.serializers import OrganizationSerializer, ProductSerializer
from server.viewset import ModelViewSet


class ProductViewSet(ModelViewSet):

    class Meta:
        model = Product
        serializer = ProductSerializer


class OrganizationViewSet(ModelViewSet):

    class Meta:
        model = Organization
        serializer = OrganizationSerializer