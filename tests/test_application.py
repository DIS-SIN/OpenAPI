from tests.base import BaseTestCase
import unittest
import json


class TestMainAppCase(BaseTestCase):
    def test_page_not_found(self):
        """
        Test that a given route does not exist in the application
        :return:
        """
        with self.client:
            response = self.client.get(
                '/home'
            )
            data = json.loads(response.data.decode())
            self.assert404(response)
            self.assertTrue(data['status'] == 'failed')
            self.assertTrue(data['message'] == 'Endpoint not found')


    def test_http_method_not_found(self):
        with self.client:
            response = self.client.delete(
                'v1/resources'
            )
            data = json.loads(response.data.decode())
            self.assert405(response)
            self.assertTrue(data['status'] == 'failed')
            self.assertTrue(data['message'] == 'The method is not allowed for the requested URL')

if __name__ == "__main__":
    unittest.main()