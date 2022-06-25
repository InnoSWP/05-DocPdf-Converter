import glob
import os
from os import path
from pathlib import Path

from django.core.files.uploadedfile import InMemoryUploadedFile
from django.http import HttpRequest
from django.test import TestCase
from django.utils.datastructures import MultiValueDict

from main.algorithm import (
    get_converted_file_path,
    save_files,
    zip_files_in_dir
)


class AlgorithmTestCase(TestCase):
    """
    class with all test algorithms
    """

    root = Path(path.dirname(__file__)).parent.absolute()

    def test_save_files_one_correct(self):
        """
        test method for saving one correct file

        :return:
        """

        files = MultiValueDict()
        with open(f"{self.root}\\test1.docx", "rb") as test_file:
            file = InMemoryUploadedFile(
                file=test_file,
                field_name=test_file,
                name="test1.docx",
                content_type="application/octet-stream",
                size=87,
                charset=None,
            )
            print(self.root)
            files["files"] = file
            http_request = HttpRequest()
            http_request.FILES = files
            self.assertEqual(
                save_files(http_request.FILES.getlist("files"), 0),
                (f"{self.root}\\main\\files\\0\\", ["test1.docx"]),
            )

    def test_save_files_two_correct(self):
        """
        test method for saving two correct files

        :return:
        """
        files, opened_files = [], []
        for file_name in ["test1.docx", "test2.docx"]:
            file = open(f"{self.root}\\{f'{file_name}'}", "rb")
            opened_files.append(file)
            files.append(
                InMemoryUploadedFile(
                    file=file,
                    field_name="files",
                    name=file_name,
                    content_type="application/octet-stream",
                    size=87,
                    charset=None,
                )
            )
        files = MultiValueDict({"files": files})
        http_request = HttpRequest()
        http_request.FILES = files
        try:
            self.assertEqual(
                save_files(http_request.FILES.getlist("files"), 0),
                (
                    f"{self.root}\\main\\files\\0\\",
                    ["test1.docx", "test2.docx"],
                ),
            )
        finally:
            for file in opened_files:
                file.close()

    def test_get_converted_file_path_correct(self):
        """
        test method for getting correct path to converted file
        :return:
        """
        self.assertEqual(
            get_converted_file_path(0),
            f"{self.root}\\main\\converted_files\\0\\",
        )

    def test_zipping_one_correct(self):
        """
        test method for zipping one file in directory
        :return:
        """
        path_to_files = f"{self.root}\\main\\converted_files\\0\\"
        files = glob.glob(f"{path_to_files}*")
        for file in files:
            os.remove(file)
        with open(f"{path_to_files}test1.pdf", "w", encoding="utf-8"):
            pass
        self.assertEqual(
            zip_files_in_dir(path_to_files, ["test1.pdf"], "result"),
            ".pdf",
        )

    def test_zipping_two_correct(self):
        """
        test method for zipping two files in directory
        :return:
        """
        path_to_files = f"{self.root}\\main\\converted_files\\1\\"
        files = glob.glob(f"{path_to_files}*")
        for file in files:
            os.remove(file)
        check_files = ["test2.pdf", "test3.pdf"]
        for file in check_files:
            with open(f"{path_to_files}{file}", "w", encoding="utf-8"):
                pass
        self.assertEqual(
            zip_files_in_dir(
                path_to_files,
                check_files,
                "result",
            ),
            ".zip",
        )
