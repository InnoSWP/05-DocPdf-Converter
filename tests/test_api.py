import os
import random
from pathlib import Path

from django.test import TestCase

from env_consts import OS_SLASH
from main.api import get_init_id


def send_single_file_response(root, client, convert_link, file_name):
    """

    :param root: root directory with file
    :param client: client sender
    :param convert_link: link for sending file
    :param file_name: name of sending file
    :return: response of request
    """
    with open(f"{root}{OS_SLASH}{file_name}", "rb") as files:
        resp = client.post(
            convert_link, {"name": "fred", "files": files, "attachment": files}
        )
    return resp


class ApiTestCase(TestCase):
    """
    class with all test algorithms
    """

    root = Path(os.path.dirname(__file__)).parent.absolute()
    first_docx = "test1.docx"
    second_docx = "test2.docx"
    convert_link = "/convert/"

    def test_convert_post_several(self):
        """
        test method for post requests

        :return:
        """
        files = []
        for file_name in ["1.docx", "2.docx", "3.docx", "4.docx", "1.xlsx"]:
            files.append(open(f"{self.root}{OS_SLASH}{file_name}", "rb"))
        resp = self.client.post(
            self.convert_link, {"name": "fred", "files": files, "attachment": files}
        )
        for file in files:
            file.close()
        self.assertEqual(
            resp.headers["files"], f"attachment; filename=result_{get_init_id()}.zip"
        )

    def test_convert_post_docx(self):
        """
        test method for post request with single docx

        :return:
        """
        file_name = "1.docx"
        resp = send_single_file_response(
            self.root, self.client, self.convert_link, file_name
        )
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(
            resp.headers["files"], f"attachment; filename=result_{get_init_id()}.pdf"
        )

    def test_convert_post_xlsx(self):
        """
        test method for post request with single xlsx

        :return:
        """
        file_name = "1.xlsx"
        resp = send_single_file_response(
            self.root, self.client, self.convert_link, file_name
        )
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(
            resp.headers["files"], f"attachment; filename=result_{get_init_id()}.pdf"
        )

    def test_convert_get_local(self):
        """
        test method for local get requests on API

        :return:
        """

        response = self.client.get(self.convert_link, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers["Content-Type"], "text/html; charset=utf-8")

    def test_convert_get_not_local(self):
        """
        test method for not local get requests on API

        :return:
        """
        response = self.client.get(
            self.convert_link,
            follow=True,
            HTTP_X_FORWARDED_FOR=".".join(
                map(str, (random.randint(0, 255) for _ in range(4)))
            ),
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers["Content-Type"], "application/json")
