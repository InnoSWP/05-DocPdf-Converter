from rest_framework import serializers
from main.models import *


class ConvertSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Converter
        fields = [
            'files',
        ]
