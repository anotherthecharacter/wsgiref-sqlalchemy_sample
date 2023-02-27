from main.models import Organization, Product
from server.serializers import ModelSerializer

from server.utils import get_object_or_404


class OrganizationSerializer(ModelSerializer):

    class Meta:
        model = Organization
        immutable_fields = (('id', int),)
        required_fields = (('title', str), ('address', str), ('category', str))
        optional_fields = tuple()


    def to_representation(self, obj):
        from server.utils import Session

        with Session() as session:
            rep = super().to_representation(obj)
            rep['category'] = obj.category.value

            return rep


class ProductSerializer(ModelSerializer):

    class Meta:
        model = Product
        immutable_fields = (('id', int),)
        required_fields = (('title', str), ('price', float), ('quantity', int), ('organization', int)) 
        optional_fields = (('description', str),)
    
    
    def to_representation(self, obj):
        from server.utils import Session

        with Session() as session:
            rep = super().to_representation(obj)
            organization = get_object_or_404(Organization, obj.organization, session)
            rep['organization'] = OrganizationSerializer().represent(organization)

            return rep
