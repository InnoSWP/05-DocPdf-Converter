import shutil

from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response

from .algorithm import convert, get_file_response, save_files, zip_files_in_dir
from .models import Conversion
from .serializers import ConvertSerializer


class ConvertApi(generics.GenericAPIView):
    """
    Main class for Convertor API.

    :param serializer_class: serializer of  :class:`models.Conversion`
    :param queryset: set of serialized objects
    """

    serializer_class = ConvertSerializer

    def post(self, request):
        """
        Post request handler for file conversion.

        :param request: request details
        :type request: :class:`rest_framework.request.Request`
        :serializer: convertSerializer formed with :class:`models.Conversion`
        :return: server response object
        :rtype: :class:`rest_framework.response.Response`
        """
        if True:
            # if 'HTTP_TOKEN' in request.META and len(request.META['HTTP_TOKEN']):
            if (
                "files" not in request.data
                or "files" in request.data
                and not request.data["files"]
            ):
                return Response(
                    {
                        "error": "invalid_files",
                        "error_description": "Files field is empty.",
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            files = request.FILES.getlist("files")
            Conversion().save()
            # Get this conversion operation id.
            last_id = Conversion.objects.latest("id").id
            acceptable_types = ["docx", "pdf"]
            # Save files and get the path to them.
            file_path, files_to_convert = save_files(files, last_id)
            # Save all filenames from request.
            # Iterate through files to get file names .
            for file in files:
                # Current file name.
                # Save acceptable file names.
                # If one of the files is not acceptable, return 400 status response.
                if not any(
                    acceptable_type in file.name for acceptable_type in acceptable_types
                ):
                    shutil.rmtree(file_path)
                    return Response(
                        {
                            "error": "invalid_file_type",
                            "error_description": "Your request has unacceptable files.",
                        },
                        status=status.HTTP_400_BAD_REQUEST,
                    )
            # Convert files and get the path to result.
            converted_file_path = convert(file_path, files_to_convert, last_id)
            # Name of the zip with a result of conversion.
            zip_name = f"result_{last_id}"
            # Save all filenames from the request.
            # Get formatted response for file.
            response = get_file_response(
                converted_file_path,
                f"{zip_name}"
                f"{zip_files_in_dir(converted_file_path, [file.name for file in files], zip_name)}",
            )
            # Remove all unnecessary directories.
            shutil.rmtree(file_path)
            shutil.rmtree(converted_file_path)
            return response
        # Return response if user not authenticated.
        return Response(
            {
                "error": "invalid_token",
                "error_description": "Your request is not authenticated.",
            },
            status=status.HTTP_401_UNAUTHORIZED,
        )

    def get(self, request):
        """
        Get request handler for showing conversion page view.

        :param request: request details
        :type request: :class:`django.http.HttpRequest`
        :return: page render object :class:`index.html`
        :rtype: :class:`django.http.HttpResponse`
        """
        if self.request_from_local(request):
            return render(request, "main/index.html", {})
        return Response(ConvertSerializer().data)

    @staticmethod
    def get_request_from(request) -> str:
        """
        Static method to get request ip address

        :param request: request details
        :type request: :class:`django.http.HttpRequest`
        :return: ip address
        :rtype: :class:`string`
        """
        ip_from = request.META.get("HTTP_X_FORWARDED_FOR")
        if ip_from:
            return ip_from
        return request.META.get("REMOTE_ADDR")

    @staticmethod
    def request_from_local(request) -> bool:
        """
        Static method to check whether it is local
        request or not

        :param request: request details
        :type request: :class:`django.http.HttpRequest`
        :return: boolean flag
        :rtype: :class:`boolean`
        """
        return ConvertApi.get_request_from(request) == "127.0.0.1"
