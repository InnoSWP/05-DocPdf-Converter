from os import path

from django.core.files.uploadedfile import InMemoryUploadedFile
from django.http import HttpRequest
from django.test import TestCase
from django.utils.datastructures import MultiValueDict
from main.algorithm import (
    get_converted_file_path,
    save_files,
    zip_files_in_dir,
)


class AlgorithmTestCase(TestCase):
    def test_save_files_one_correct(self):
        files = MultiValueDict()
        file = InMemoryUploadedFile(
            file=open(f"{path.dirname(__file__)[:-11]}\\test1.docx", "rb"),
            field_name="files",
            name="test1.docx",
            content_type="application/octet-stream",
            size=87,
            charset=None,
        )
        files["files"] = file
        http_request = HttpRequest()
        http_request.FILES = files
        self.assertEqual(
            save_files(http_request.FILES.getlist("files"), 0),
            (f"{path.dirname(__file__)[:-6]}\\files\\0\\", ["test1.docx"]),
        )

    def test_save_files_two_correct(self):
        file1 = InMemoryUploadedFile(
            file=open(f"{path.dirname(__file__)[:-11]}\\test1.docx", "rb"),
            field_name="files",
            name="test1.docx",
            content_type="application/octet-stream",
            size=87,
            charset=None,
        )
        file2 = InMemoryUploadedFile(
            file=open(f"{path.dirname(__file__)[:-11]}\\test2.docx", "rb"),
            field_name="files",
            name="test2.docx",
            content_type="application/octet-stream",
            size=87,
            charset=None,
        )
        files = MultiValueDict({"files": [file1, file2]})
        http_request = HttpRequest()
        http_request.FILES = files
        self.assertEqual(
            save_files(http_request.FILES.getlist("files"), 0),
            (
                f"{path.dirname(__file__)[:-6]}\\files\\0\\",
                ["test1.docx", "test2.docx"],
            ),
        )

    def test_get_converted_file_path_correct(self):
        self.assertEqual(
            get_converted_file_path(0),
            f"{path.dirname(__file__)[:-6]}\\converted_files\\0\\",
        )

    def test_get_converted_file_path_incorrect(self):
        self.assertEqual(
            get_converted_file_path(0), f"{path.dirname(__file__)[:-6]}\\wrong_path"
        )

    def test_zipping_one_correct(self):
        self.assertEqual(
            zip_files_in_dir(
                f"{path.dirname(__file__)[:-11]}\\", ["test1.pdf"], "result"
            ),
            ".pdf",
        )

    def test_zipping_two_correct(self):
        self.assertEqual(
            zip_files_in_dir(
                f"{path.dirname(__file__)[:-11]}\\",
                ["test1.pdf", "test2.pdf"],
                "result",
            ),
            ".zip",
        )
