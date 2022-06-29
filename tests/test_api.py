import os
from pathlib import Path

from django.test import TestCase

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "djangoApp.settings")
import django

django.setup()
from env_consts import OS_SLASH


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
        self.assertEqual(resp.headers["files"], f"attachment; filename=result_1.zip")

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
        self.assertEqual(resp.headers["files"], f"attachment; filename=result_1.pdf")