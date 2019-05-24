from flask import Blueprint, request, abort
from app.resources.helper import response, response_for_created_resource, response_for_resource, response_with_pagination, get_resources_json_list, paginate_resources
from app.models import Resource

# Initialize blueprint
resources = Blueprint('resources', __name__)


@resources.route('/resources', methods=['GET'])
def resourcelist():
    """
    Return all the resources or limit them to a certain count.
    Return an empty resource object if no resources
    :return:
    """
    
    page = request.args.get('page', 1, type=int)
    q = request.args.get('q', None, type=str)

    items, nex, pagination, previous = paginate_resources(page, q)

    if items:
        return response_with_pagination(get_resources_json_list(items), previous, nex, pagination.total)
    return response_with_pagination([], previous, nex, 0)


@resources.route('/resources', methods=['POST'])
def create_resource():
    """
    Create an resource from the sent json data.
    :return:
    """
    if request.content_type == 'application/json':
        data = request.get_json().get("resource")
        link = data.get('link') if data.get('link') is not None else None
        categories = data.get('categories') if data.get('categories') is not None else None
        status = data.get('status') if data.get('status') is not None else None 
        if link and categories and status:
            resource = Resource(link, categories, status)
            resource.save()
            return response_for_created_resource(resource, 201)
        return response('failed', 'Missing some resource data, nothing was changed', 400)
    return response('failed', 'Content-type must be json', 202)


@resources.route('/resources/<resource_id>', methods=['GET'])
def get_resource(resource_id):
    """
    Return a resource.
    :param resource_id: resource Id
    :return:
    """
    try:
        int(resource_id)
    except ValueError:
        return response('failed', 'Please provide a valid resource Id', 400)
    else:
        resource = Resource.query.filter_by(resource_id=resource_id).first()
        if resource:
            return response_for_resource(resource.json())
        return response('failed', "Resource not found", 404)


@resources.route('/resources/<resource_id>', methods=['PUT'])
def edit_resource(resource_id):
    """
    Validate the resource Id. Also check for the data in the json payload.
    If the data exists update the resource with the new data.
    :param resource_id: resource Id
    :return: Http Json response
    """
    if request.content_type == 'application/json':
        data = request.get_json().get("resource")
        link = data.get('link') if data.get('link') is not None else None
        categories = data.get('categories') if data.get('categories') is not None else None
        status = data.get('status') if data.get('status') is not None else None 
        updated_resource = Resource(link, categories, status)
        if link or categories or status:
            try:
                int(resource_id)
            except ValueError:
                return response('failed', 'Please provide a valid resource Id', 400)
            resource = Resource.query.filter_by(resource_id=resource_id).first()
            if resource:
                resource.update(updated_resource)
                return response_for_created_resource(resource, 201)
            return response('failed', 'The resource with Id ' + resource_id + ' does not exist', 404)
        return response('failed', 'No attribute or value was specified, nothing was changed', 400)
    return response('failed', 'Content-type must be json', 202)


@resources.route('/resources/<resource_id>', methods=['DELETE'])
def delete_resource(resource_id):
    """
    Deleting a resource from the database if it exists.
    :param resource_id:
    :return:
    """
    try:
        int(resource_id)
    except ValueError:
        return response('failed', 'Please provide a valid resource Id', 400)
    resource = Resource.query.filter_by(resource_id=resource_id).first()
    if not resource:
        abort(404)
    resource.delete()
    return response('success', 'Resource deleted successfully', 200)


@resources.errorhandler(404)
def handle_404_error(e):
    """
    Return a custom message for 404 errors.
    :param e:
    :return:
    """
    return response('failed', 'Resource cannot be found', 404)


@resources.errorhandler(400)
def handle_400_errors(e):
    """
    Return a custom response for 400 errors.
    :param e:
    :return:
    """
    return response('failed', 'Bad Request', 400)
