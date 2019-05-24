from tests.base import BaseTestCase
import unittest
import json


class TestresourceBluePrint(BaseTestCase):
    def test_creating_a_resource(self):
        """
        Test that a user can add a resource
        :return:
        """
        with self.client:
            self.create_resource()

    def test_missing_attributes_is_set_in_resource_creation_request(self):
        """
        Test that some attribute are present in the json request.
        :return:
        """
        with self.client:
            response = self.client.post(
                'v1/resources',
                data=json.dumps({"resource":{}}),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertTrue(data['status'], 'failed')
            self.assertTrue(data['message'], 'Missing some resource data, nothing was changed')

    def test_resource_post_content_type_is_json(self):
        """
        Test that the request content type is application/json
        :return:
        """
        with self.client:
            response = self.client.post(
                'v1/resources',
                data=json.dumps(dict(resource = dict(link = "hhtp://google.ca", categories="AI;ML;Data-science", status = "Pending")))
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 202)
            self.assertTrue(data['status'], 'failed')
            self.assertTrue(data['message'], 'Content-type must be json')

    def test_get_list_of_resources(self):
        """
        Test that getting a list resources or an empty dictionary if there isn't any
        :return:
        """
        with self.client:
            response = self.client.get(
                'v1/resources'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertTrue(data['status'] == 'success')
            self.assertIsInstance(data['resources'], list)
            self.assertEqual(len(data['resources']), 0)
            self.assertEqual(data['count'], 0)
            self.assertIsInstance(data['count'], int)
            self.assertEqual(data['previous'], None)
            self.assertEqual(data['next'], None)

    def test_request_for_a_resource_has_integer_id(self):
        """
        Test that only integer resource Ids are allowed
        :return:
        """
        with self.client:
            response = self.client.get(
                'v1/resources/dsfgsdsg'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertTrue(data['status'] == 'failed')
            self.assertTrue(data['message'] == 'Please provide a valid resource Id')

    def test_resource_by_id_is_returned_on_get_request(self):
        """
        Test that a user resource is returned when a specific Id is specified
        :return:
        """
        with self.client:            
            # Create and test a resource
            self.create_resource()
            
            response = self.client.get(
                'v1/resources/1'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertTrue(data['status'], 'success')
            self.assertTrue(data['resource']['link'], 'http://google.com')
            self.assertTrue(data['resource']['categories'], 'AI;ML;Data-science')
            self.assertTrue(data['resource']['status'], 'Pending')
            self.assertIsInstance(data['resource'], dict)
            self.assertTrue(response.content_type == 'application/json')

    def test_no_resource_returned_by_given_id(self):
        """
        Test there is no resource/no resource returned with given Id
        :return:
        """
        with self.client:
            response = self.client.get(
                'v1/resources/1'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertTrue(data['status'] == 'failed')
            self.assertTrue(data['message'] == 'Resource not found')
            self.assertTrue(response.content_type == 'application/json')

    def test_deletion_handles_no_resource_found_by_id(self):
        """
        Show that a 404 response is returned when an un existing resource is being deleted.
        :return:
        """
        with self.client:
            response = self.client.delete(
                'v1/resources/1'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertTrue(data['status'] == 'failed')
            self.assertTrue(data['message'] == 'Resource cannot be found')
            self.assertTrue(response.content_type == 'application/json')

    def test_request_for_deleting_resource_has_integer_id(self):
        """
        Test that only integer resource Ids are allowed
        :return:
        """
        with self.client:
            response = self.client.delete(
                'v1/resources/dsfgsdsg'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertTrue(data['status'] == 'failed')
            self.assertTrue(data['message'] == 'Please provide a valid resource Id')

    def test_resource_is_updated(self):
        """
        Test that the resource details(name) is updated
        :return:
        """
        with self.client:
            # Create a resource
            response = self.client.post(
                'v1/resources',
                data=json.dumps(dict(resource = dict(link = "hhtp://google.ca", categories="AI;ML;Data-science", status = "Pending"))),
                headers=dict(Authorization='Bearer ' + token),
                content_type='application/json'
            )

            # Test resource creation
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertTrue(data['status'], 'success')
            self.assertTrue(data['resource']['link'], 'http://google.com')
            self.assertTrue(data['resource']['categories'], 'AI;ML;Data-science')
            self.assertTrue(data['resource']['status'], 'Pending')


    def test_resource_is_updated(self):
        """
        Test that the resource details(name) is updated
        :return:
        """
        with self.client:
            # Create and test resource creation
            self.create_resource()            

            # Update the resource link
            res = self.client.put(
                'v1/resources/1',
                data=json.dumps(dict(resource = dict(link = "http://youtube.com"))),
                content_type='application/json'
            )
            data = json.loads(res.data.decode())
            self.assertEqual(res.status_code, 201)
            self.assertTrue(res.content_type == 'application/json')
            self.assertTrue(data['status'], 'success')
            self.assertTrue(data['resource']['link'], 'http://youtube.com')
            self.assertEqual(data['resource']['id'], 1)

            # Update the resource categories
            res = self.client.put(
                'v1/resources/1',
                data=json.dumps(dict(resource = dict(categories = "Physics"))),
                content_type='application/json'
            )
            data = json.loads(res.data.decode())
            self.assertEqual(res.status_code, 201)
            self.assertTrue(res.content_type == 'application/json')
            self.assertTrue(data['status'], 'success')
            self.assertTrue(data['resource']['categories'], 'Physics')
            self.assertEqual(data['resource']['id'], 1)

            # Update the resource time
            res = self.client.put(
                'v1/resources/1',
                data=json.dumps(dict(resource = dict(status = "Approved"))),
                content_type='application/json'
            )
            data = json.loads(res.data.decode())
            self.assertEqual(res.status_code, 201)
            self.assertTrue(res.content_type == 'application/json')
            self.assertTrue(data['status'], 'success')
            self.assertTrue(data['resource']['status'], 'Approved')
            self.assertEqual(data['resource']['id'], 1)

    def test_id_of_resource_to_be_edited_does_not_exist(self):
        """
        Test the resource to be updated does not exist.
        :return:
        """
        with self.client:
            # Update the resource link
            res = self.client.put(
                'v1/resources/1',
                data=json.dumps(dict(resource = dict(link = "http://youtube.com"))),
                content_type='application/json'
            )
            data = json.loads(res.data.decode())
            self.assertEqual(res.status_code, 404)
            self.assertTrue(res.content_type == 'application/json')
            self.assertTrue(data['status'] == 'failed')
            self.assertTrue(data['message'] == 'The resource with Id 1 does not exist')

    def test_id_of_resource_to_be_edited_is_invalid(self):
        """
        Test the resource id is invalid.
        :return:
        """
        with self.client:
            # Update the resource link
            res = self.client.put(
                'v1/resources/resourceid',
                data=json.dumps(dict(resource = dict(link = "http://youtube.com"))),
                content_type='application/json'
            )
            data = json.loads(res.data.decode())
            self.assertEqual(res.status_code, 400)
            self.assertTrue(res.content_type == 'application/json')
            self.assertTrue(data['status'] == 'failed')
            self.assertTrue(data['message'] == 'Please provide a valid resource Id')

    def test_content_type_for_editing_resource_is_json(self):
        """
        Test that the content type used for the request is application/json
        :return:
        """
        with self.client:            
            res = self.client.put(
                'v1/resources/1',
                data=json.dumps(dict(resource = dict(link = "hhtp://google.ca")))
            )
            data = json.loads(res.data.decode())
            self.assertEqual(res.status_code, 202)
            self.assertTrue(data['status'] == 'failed')
            self.assertTrue(data['message'] == 'Content-type must be json')

    def test_required_link_attribute_is_in_the_request_payload_and_has_a_value(self):
        """
        Test that the required attribute(link) exists and has value in the request payload
        :return:
        """
        with self.client:
            res = self.client.put(
                'v1/resources/1',
                data=json.dumps(dict(resource = dict(link = ""))),
                content_type='application/json'
            )
            data = json.loads(res.data.decode())
            self.assertEqual(res.status_code, 400)
            self.assertTrue(data['status'] == 'failed')
            self.assertTrue(data['message'] == 'No attribute or value was specified, nothing was changed')

    def test_required_categories_attribute_is_in_the_request_payload_and_has_a_value(self):
        """
        Test that the required attribute(categories) exists and has value in the request payload
        :return:
        """
        with self.client:
            
            res = self.client.put(
                'v1/resources/1',
                data=json.dumps(dict(resource = dict(categories=""))),
                content_type='application/json'
            )
            data = json.loads(res.data.decode())
            self.assertEqual(res.status_code, 400)
            self.assertTrue(data['status'] == 'failed')
            self.assertTrue(data['message'] == 'No attribute or value was specified, nothing was changed')

    def test_required_status_attribute_is_in_the_request_payload_and_has_a_value(self):
        """
        Test that the required attribute(status) exists and has value in the request payload
        :return:
        """
        with self.client:            
            res = self.client.put(
                'v1/resources/1',
                data=json.dumps(dict(resource = dict(status = ""))),
                content_type='application/json'
            )
            data = json.loads(res.data.decode())
            self.assertEqual(res.status_code, 400)
            self.assertTrue(data['status'] == 'failed')
            self.assertTrue(data['message'] == 'No attribute or value was specified, nothing was changed')

    def test_resource_is_deleted(self):
        """
        Test that a resource is deleted successfully
        :return:
        """
        with self.client:
            # Test and create a resource
            self.create_resource()
            
            # Delete the created resource
            res = self.client.delete(
                'v1/resources/1'
            )
            data = json.loads(res.data.decode())
            self.assertEqual(res.status_code, 200)
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] == 'Resource deleted successfully')
            self.assertTrue(res.content_type == 'application/json')

    def test_resources_returned_when_searched(self):
        """
        Test resources are returned when a query search q is present in the url
        Also test that the next page pagination string is 'http://localhost/resources?page=2'
        and previous is none
        :return:
        """
        with self.client:
            # Create and test resources
            self.create_resources()

            # Test get resources with query search
            response = self.client.get(
                'v1/resources?q=com'
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertIsInstance(data['resources'], list, 'Items must be a list')
            self.assertEqual(len(data['resources']), 4)
            self.assertEqual(data['resources'][0]['id'], 1)
            self.assertEqual(data['count'], 5)
            self.assertEqual(data['next'], 'http://localhost/v1/resources?q=com&page=2')
            self.assertEqual(data['previous'], None)
            self.assertEqual(response.status_code, 200)

    def test_resources_returned_when_searched_2(self):
        """
        Test resources are returned when a query search q is present in the url
        Also test that the next page pagination string is None
        and previous is 'http://localhost/resources?page=1'
        :return:
        """
        with self.client:
            # Create and test resources
            self.create_resources()

            response = self.client.get(
                'v1/resources?q=com&page=2'
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertIsInstance(data['resources'], list, 'Items must be a list')
            self.assertEqual(len(data['resources']), 1)
            self.assertEqual(data['resources'][0]['id'], 5)
            self.assertEqual(data['count'], 5)
            self.assertEqual(data['next'], None)
            self.assertEqual(data['previous'], 'http://localhost/v1/resources?q=com&page=1')
            self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
