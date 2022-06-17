from rest_framework import serializers
from main.models import Converter


class ConvertSerializer(serializers.HyperlinkedModelSerializer):
    """
    Convert serializer

    :param Meta: class with metadata
    """
    class Meta:
        """
        Metadata

        :param model: converter
        :type model: :class:`main.models.Converter`
        :param fields: serializer fields
        :type fields: :class:`list of strings`
        """
        model = Converter
        fields = [
            'files',
        ]
