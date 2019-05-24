from app import app, db
from flask_testing import TestCase
import json


class BaseTestCase(TestCase):
    def create_app(self):
        """
        Create an instance of the app with the testing configuration
        :return:
        """
        app.config.from_object('app.config.TestingConfig')
        return app

    def setUp(self):
        """
        Create the database
        :return:
        """
        db.create_all()
        db.session.commit()

    def tearDown(self):
        """
        Drop the database tables and also remove the session
        :return:
        """
        db.session.remove()
        db.drop_all()

    def create_resource(self):
        """
        Helper function to create a resource
        :return:
        """
        response = self.client.post(
            'v1/resources',
            data=json.dumps(dict(resource = dict(link = "http://google.com", categories="AI;ML;Data-science", status = "Pending"))),
            content_type='application/json'
        )
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 201)
        self.assertTrue(data['status'], 'success')
        self.assertTrue(data['resource']['link'], 'http://google.com')
        self.assertTrue(data['resource']['categories'], 'AI;ML;Data-science')
        self.assertTrue(data['resource']['status'], 'Pending')
        self.assertIsInstance(data['resource']['id'], int, msg='Value should be a string')

    def create_resources(self):
        '''
        Helper function to create an resource
        :return:
        '''
        resources = [
            {'resource': {'link' : 'http://facebook.com', 'categories' : 'AI', 'status' : 'Pending'}},
            {'resource': {'link' : 'http://youtube.com', 'categories' : 'ML', 'status' : 'Approved'}},
            {'resource': {'link' : 'http://web.whatsapp.com', 'categories' : 'Data science', 'status' : 'Pending'}},
            {'resource': {'link' : 'http://twitter.com', 'categories' : 'Statistics', 'status' : 'Approved'}},
            {'resource': {'link' : 'http://google.com', 'categories' : 'Math', 'status' : 'Pending'}},
            {'resource': {'link' : 'https://csps-efpc.gc.ca', 'categories' : 'Languages', 'status' : 'Approved'}}
        ]
        for resource in resources:
            response = self.client.post(
                'v1/resources',
                data=json.dumps(dict(resource)),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertTrue(data['status'], 'success')
            self.assertTrue(data['resource']['link'], resource['resource']['link'])
            self.assertTrue(data['resource']['categories'], resource['resource']['categories'])
            self.assertTrue(data['resource']['status'], resource['resource']['status'])
            self.assertIsInstance(data['resource']['id'], int, msg='Value should be a string')