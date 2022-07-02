from django.test import TestCase


class ApiTestCase(TestCase):
    """
    Test class for API
    """
    def test_index_page_get(self):
        """
        test method for getting main page

        :return:
        """
        response = self.client.get("/convert/", follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers["Content-Type"], "text/html; charset=utf-8")
