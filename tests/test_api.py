import os
from pathlib import Path

from django.test import TestCase
import pytest

from env_consts import OS_SLASH


@pytest.mark.transactional_db
class ApiTestCase(TestCase):
    """
    class with all test algorithms
    """

    root = Path(os.path.dirname(__file__)).parent.absolute()
    first_docx = "test1.docx"
    second_docx = "test2.docx"

    def test_convert_post_several(self):
        """
        test method for post requests

        :return:
        """
        files = []
        for file_name in ["1.docx", "2.docx", "3.docx", "4.docx"]:
            files.append(open(f"{self.root}{OS_SLASH}{file_name}", "rb"))
        resp = self.client.post(
            "/convert/", {"name": "fred", "files": files, "attachment": files}
        )
        for file in files:
            file.close()
        self.assertEqual(resp.headers["files"], "attachment; filename=result_1.zip")

    def test_convert_post_one(self):
        """
        test method for post requests

        :return:
        """
        file_name = "1.docx"
        with open(f"{self.root}{OS_SLASH}{file_name}", "rb") as files:
            resp = self.client.post(
                "/convert/", {"name": "fred", "files": files, "attachment": files}
            )
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.headers["files"], "attachment; filename=result_1.pdf")

    def test_convert_get_local(self):
        """
        test method for local get requests on API

        :return:
        """

        response = self.client.get("/convert/", follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers["Content-Type"], "text/html; charset=utf-8")

    def test_convert_get_not_local(self):
        """
        test method for not local get requests on API

        :return:
        """
        response = self.client.get(
            "/convert/", follow=True, HTTP_X_FORWARDED_FOR="189.130.155.154"
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers["Content-Type"], "application/json")
