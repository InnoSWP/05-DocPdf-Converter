import os
import shutil
from os import path
from pathlib import Path

import env_consts as ec
from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response

from .algorithm import (
    convert,
    get_converted_file_path,
    get_file_response,
    save_files,
    zip_files_in_dir,
)
from .serializers import ConvertSerializer


def get_init_id():
    """
    Get id from file.

    :return: id
    :rtype: int
    """
    with open(ec.LAST_OP_FILE, "r", encoding="utf-8") as file:
        line = file.read()
        if not line:
            return 0
        return int(line)


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
            # if 'HTTP_TOKEN' in request.META and
            # len(request.META['HTTP_TOKEN']):
            bad_request = False
            try:
                if (
                    "files" not in request.data
                    or "files" in request.data
                    and not request.data["files"]
                ):
                    bad_request = True
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
                Path(ec.LAST_OP_FILE).touch(exist_ok=True)
                init_id = get_init_id()
                # Get this conversion operation id.
                with open(ec.LAST_OP_FILE, "w", encoding="utf-8") as file:
                    file.write(str(init_id + 1))
                last_id = get_init_id()
                acceptable_types = {
                    ".docx": False,
                    ".xlsx": False,
                    ".pdf": False,
                    ".doc": False,
                    ".xls": False,
                }
                # Save files and get the path to them.
                for file in files:
                    # If one of the files is not acceptable, return 400 status
                    # response.
                    if not any(
                        acceptable_type == os.path.splitext(file.name)[1]
                        for acceptable_type in acceptable_types
                    ):
                        bad_request = True
                        return Response(
                            {
                                "error": "invalid_file_type",
                                "error_description": "Your request has unacceptable files.",
                            },
                            status=status.HTTP_400_BAD_REQUEST,
                        )
                    acceptable_types[os.path.splitext(file.name)[1]] = True
                # Save all files from request.
                file_path, files_to_convert = save_files(files, last_id)
                # Convert files and get the path to result.
                converted_file_path = convert(
                    file_path, files_to_convert, last_id, acceptable_types
                )
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
                return response
            except Exception as exception:
                print(exception)
            finally:
                if not bad_request:
                    last_id = get_init_id()
                    file_path = f"{path.dirname(__file__)}{ec.OS_SLASH}files{ec.OS_SLASH}{last_id}{ec.OS_SLASH}"
                    shutil.rmtree(file_path)
                    shutil.rmtree(get_converted_file_path(last_id))

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
