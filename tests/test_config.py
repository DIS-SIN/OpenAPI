from flask_testing import TestCase
from app import app
from flask import current_app
import unittest
import os


class TestDevelopmentConfig(TestCase):
    def create_app(self):
        """
        Create an app with the development configuration
        :return:
        """
        app.config.from_object('app.config.DevelopmentConfig')
        return app

    def test_app_in_development(self):
        """
        Test that the development configs are set correctly.
        :return:
        """
        self.assertTrue(app.config['DEBUG'], True)
        self.assertFalse(current_app is None)
        self.assertTrue(app.config['SQLALCHEMY_DATABASE_URI'] == os.getenv('DATABASE_URL',
                                                                           "postgresql://postgres:password@localhost/openapi"))
        self.assertEqual(app.config['RESOURCES_PER_PAGE'], 4)


class TestTestingConfig(TestCase):
    def create_app(self):
        """
        Create an instance of the app with the testing configuration
        :return:
        """
        app.config.from_object('app.config.TestingConfig')
        return app

    def test_app_in_testing(self):
        """
        Test that the testing configs are set correctly
        :return:
        """
        self.assertFalse(current_app is None)
        self.assertTrue(app.config['SQLALCHEMY_DATABASE_URI'] == os.getenv('DATABASE_URL_TEST', "postgresql://postgres:password@localhost/openapi_test"))
        self.assertEqual(app.config['RESOURCES_PER_PAGE'], 4)


if __name__ == '__main__':
    unittest.main()
