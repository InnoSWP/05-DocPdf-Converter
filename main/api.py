import os
import shutil

from django.http import HttpResponse
from rest_framework import generics, status
from rest_framework.response import Response
from os import makedirs, path
from .algorithm import convert, zip_files_in_dir
from .models import Converter, Conversion
from .serializers import ConvertSerializer


class ConvertApi(generics.GenericAPIView):
    serializer_class = ConvertSerializer
    queryset = Converter.objects.all()

    def post(self, request, *args,  **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if 'HTTP_TOKEN' in request.META and len(request.META['HTTP_TOKEN']):
            if 'files' in request.data and not len(request.data['files']):
                return Response(
                    {
                        "error": "invalid_files",
                        "error_description": "Files field is empty.",
                    }, status=status.HTTP_400_BAD_REQUEST
                )
            files = request.FILES.getlist('files')
            conversion = Conversion()
            conversion.save()
            last_id = Conversion.objects.latest('id').id
            filepath = f'{path.dirname(__file__)}/files/{last_id}/'
            for file in files:
                makedirs(filepath, exist_ok=True)
                filename = f'{filepath}{file.name}'
                with open(filename, 'wb') as out_file:
                    shutil.copyfileobj(file, out_file)
            file_names = [file.name for file in files]
            convert(filepath, files, last_id)
            zip_files_in_dir(filepath, file_names, "sample.zip")
            zip_file = open(f'{filepath}sample.zip', 'rb')
            response = HttpResponse(zip_file, content_type='application/zip')
            response['files'] = 'attachment; filename=sample.zip'
            zip_file.close()
            shutil.rmtree(filepath)
            return response
        else:
            return Response({
                "error": "invalid_token",
                "error_description": "Your request is not authentificated.",
            }, status=status.HTTP_401_UNAUTHORIZED)

