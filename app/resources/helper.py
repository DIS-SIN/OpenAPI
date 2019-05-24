from flask import make_response, jsonify, url_for
from app import app, db
from app.models import Resource


def response_for_resource(resource):
    """
    Return the response for when a single resource was requested.
    :param resource:
    :return:
    """
    return make_response(jsonify({
        'status': 'success',
        'resource': resource
    }))


def response_for_created_resource(resource, status_code):
    """
    Method returning the response when an resource has been successfully created.
    :param status_code:
    :param resource: resource
    :return: Http Response
    """
    return make_response(jsonify({'resource' : {
        'id': resource.resource_id,
        'link': resource.resource_link,
        'categories': resource.resource_categories,
        'status': resource.resource_status,
        'created_on': resource.resource_created_on,
        'modified_on': resource.resource_updated_on
    }, 'status': 'success'})), status_code


def response(status, message, code):
    """
    Helper method to make a http response
    :param status: Status message
    :param message: Response message
    :param code: Response status code
    :return: Http Response
    """
    return make_response(jsonify({
        'status': status,
        'message': message
    })), code


def get_resources_json_list(all_resources):
    """
    Make json objects of the resources and add them to a list.
    :param resources: resource
    :return:
    """
    resources = []
    for resource in all_resources:
        resources.append(resource.json())
    return resources


def response_with_pagination(resources, previous, nex, count):
    """
    Make a http response for resourceList get requests.
    :param count: Pagination Total
    :param nex: Next page Url if it exists
    :param previous: Previous page Url if it exists
    :param resources: resource
    :return: Http Json response
    """
    return make_response(jsonify({
        'status': 'success',
        'previous': previous,
        'next': nex,
        'count': count,
        'resources': resources
    })), 200


def paginate_resources(page, q):
    """
    Get the resources and also paginate the results.
    There is also an option to search for an resource link if the query param is set.
    Generate previous and next pagination urls
    :param q: Query parameter
    :param page: Page number
    :return: Pagination next url, previous url and the resources.
    """
    if q:
        pagination = Resource.query.filter(Resource.resource_link.like("%" + q.lower().strip() + "%")).paginate(page=page, per_page=app.config['RESOURCES_PER_PAGE'], error_out=False)
    else:
        pagination = Resource.query.paginate(page=page, per_page=app.config['RESOURCES_PER_PAGE'], error_out=False)
    previous = None
    if pagination.has_prev:
        if q:
            previous = url_for('resources.resourcelist', q=q, page=page - 1, _external=True)
        else:
            previous = url_for('resources.resourcelist', page=page - 1, _external=True)
    nex = None
    if pagination.has_next:
        if q:
            nex = url_for('resources.resourcelist', q=q, page=page + 1, _external=True)
        else:
            nex = url_for('resources.resourcelist', page=page + 1, _external=True)
    items = pagination.items
    return items, nex, pagination, previous