import shutil
from rest_framework import generics, permissions, mixins, settings, status
from rest_framework.response import Response

from .algorithm import convert
from .models import Converter
from .serializers import ConvertSerializer


class ConvertApi(generics.GenericAPIView):
    serializer_class = ConvertSerializer
    queryset = Converter.objects.all()

    def post(self, request, *args,  **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if 'token' in request.data:
            files = request.FILES.getlist('files')
            for file in files:
                with open(file.name, 'wb') as out_file:
                    shutil.copyfileobj(file, out_file)
            return Response({
                "files": f'{convert(files)}'
            })
        else:
            return Response({
                "error": "invalid_token",
                "error_description": "Your request is not authentificated.",
            }, status=status.HTTP_401_UNAUTHORIZED)

