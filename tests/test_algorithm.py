import glob
import os
from os import path
from pathlib import Path

import main.algorithm as main_a
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.http import HttpRequest
from django.test import TestCase
from django.utils.datastructures import MultiValueDict

from env_consts import OS_SLASH


class AlgorithmTestCase(TestCase):
    """
    class with all test algorithms
    """

    root = Path(path.dirname(__file__)).parent.absolute()
    first_docx = "test1.docx"
    second_docx = "test2.docx"


    def test_save_files_one_correct(self):
        """
        test function for saving one correct file

        :return:
        """

        files = MultiValueDict()
        with open(
            f"{self.root}{OS_SLASH}{self.first_docx}", "a+", encoding="utf-8"
        ) as test_file:
            file = InMemoryUploadedFile(
                file=test_file,
                field_name=test_file,
                name=self.first_docx,
                content_type="application/octet-stream",
                size=87,
                charset=None,
            )
            files["files"] = file
            http_request = HttpRequest()
            http_request.FILES = files
            self.assertEqual(
                main_a.save_files(http_request.FILES.getlist("files"), 0),
                (
                    f"{self.root}{OS_SLASH}main{OS_SLASH}"
                    f"files{OS_SLASH}0{OS_SLASH}",
                    [self.first_docx],
                ),
            )

    def test_save_files_two_correct(self):
        """
        test function for saving two correct files

        :return:
        """
        files, opened_files = [], []
        for file_name in [self.first_docx, self.second_docx]:
            file = open(
                f"{self.root}{OS_SLASH}{f'{file_name}'}", "a+", encoding="utf-8"
            )
            opened_files.append(file)
            files.append(
                InMemoryUploadedFile(
                    file=file,
                    field_name="files",
                    name=file_name,
                    content_type=MimeTypes().guess_type(file_name),
                    size=87,
                    charset=None,
                )
            )
        files = MultiValueDict({"files": files})
        http_request = HttpRequest()
        http_request.FILES = files
        try:
            self.assertEqual(
                main_a.save_files(http_request.FILES.getlist("files"), 0),
                (
                    f"{self.root}{OS_SLASH}main{OS_SLASH}"
                    f"files{OS_SLASH}0{OS_SLASH}",
                    [self.first_docx, self.second_docx],
                ),
            )
        finally:
            for file in opened_files:
                file.close()

    def test_save_two_different_files(self):
        """
        test function for saving two different files

        :return:
        """
        files, opened_files = [], []
        files_list = [self.first_docx, "just.pdf"]
        for file_name in files_list:
            file = open(
                f"{self.root}{OS_SLASH}{f'{file_name}'}", "a+", encoding="utf-8"
            )
            opened_files.append(file)
            files.append(
                InMemoryUploadedFile(
                    file=file,
                    field_name="files",
                    name=file_name,
                    content_type=MimeTypes().guess_type(file_name),
                    size=87,
                    charset=None,
                )
            )
        files = MultiValueDict({"files": files})
        http_request = HttpRequest()
        http_request.FILES = files
        try:
            self.assertEqual(
                main_a.save_files(http_request.FILES.getlist("files"), 0),
                (
                    f"{self.root}{OS_SLASH}main{OS_SLASH}"
                    f"files{OS_SLASH}0{OS_SLASH}",
                    [self.first_docx],
                ),
            )
        finally:
            for file in opened_files:
                file.close()

    def test_get_converted_file_path_correct(self):
        """
        test function for getting correct path to converted file
        :return:
        """
        self.assertEqual(
            main_a.get_converted_file_path(0),
            f"{self.root}{OS_SLASH}main{OS_SLASH}converted_files{OS_SLASH}0"
            f"{OS_SLASH}",
        )

    def test_zipping_one_correct(self):
        """
        test function for zipping one file in directory
        :return:
        """
        path_to_files = (
            f"{self.root}{OS_SLASH}main{OS_SLASH}converted_files{OS_SLASH}0{OS_SLASH}"
        )
        files = glob.glob(f"{path_to_files}*")
        for file in files:
            os.remove(file)
        os.makedirs(path_to_files, exist_ok=True)
        with open(f"{path_to_files}test1.pdf", "w", encoding="utf-8"):
            pass
        self.assertEqual(
            main_a.zip_files_in_dir(path_to_files, ["test1.pdf"], "result"),
            ".pdf",
        )

    def test_zipping_two_correct(self):
        """
        test function for zipping two files in directory
        :return:
        """
        path_to_files = (
            f"{self.root}{OS_SLASH}main{OS_SLASH}converted_files{OS_SLASH}1{OS_SLASH}"
        )
        files = glob.glob(f"{path_to_files}*")
        for file in files:
            os.remove(file)
        check_files = ["test2.pdf", "test3.pdf"]
        os.makedirs(path_to_files, exist_ok=True)
        for file in check_files:
            with open(f"{path_to_files}{file}", "w", encoding="utf-8"):
                pass
        self.assertEqual(
            main_a.zip_files_in_dir(
                path_to_files,
                check_files,
                "result",
            ),
            ".zip",
        )

    def test_converting_one_docx(self):
        """
        test function for converting one docx
        :return:
        """
        index = 0
        path_to_files = (
            f"{self.root}{OS_SLASH}main{OS_SLASH}files{OS_SLASH}{index}{OS_SLASH}"
        )
        os.makedirs(path_to_files, exist_ok=True)
        files = [self.first_docx]
        with open(f"{path_to_files}test1.docx", "w", encoding="utf-8"):
            pass
        self.assertEqual(
            main_a.convert(path_to_files, files, index),
            f"{self.root}{OS_SLASH}main{OS_SLASH}converted_files{OS_SLASH}{index}{OS_SLASH}",
        )

    def test_converting_two_docx(self):
        """
        test function for converting two docx
        :return:
        """
        index = 0
        path_to_files = (
            f"{self.root}{OS_SLASH}main{OS_SLASH}files{OS_SLASH}{index}{OS_SLASH}"
        )
        os.makedirs(path_to_files, exist_ok=True)
        files = [self.first_docx, self.second_docx]
        for file in files:
            with open(f"{path_to_files}{file}", "w", encoding="utf-8"):
                pass
        self.assertEqual(
            main_a.convert(path_to_files, files, index),
            f"{self.root}{OS_SLASH}main{OS_SLASH}converted_files{OS_SLASH}{index}{OS_SLASH}",
        )
