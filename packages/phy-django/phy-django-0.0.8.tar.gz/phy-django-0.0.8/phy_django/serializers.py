from rest_framework.serializers import *
from rest_framework.serializers import HyperlinkedModelSerializer as _HyperlinkedModelSerializer

__keep = (Serializer,)


class HyperlinkedModelSerializer(_HyperlinkedModelSerializer):
    class Meta:
        pass
