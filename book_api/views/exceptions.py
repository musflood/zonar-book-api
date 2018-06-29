"""JSON responses for various HTTP exceptions."""

from pyramid.httpexceptions import HTTPBadRequest, HTTPForbidden
from pyramid.view import notfound_view_config, exception_view_config


@notfound_view_config(renderer='json')
def notfound_view(request):
    """Get JSON response for a 404 status code."""
    request.response.status = 404
    return {'message': 'Page not found.', 'status': 404}


@exception_view_config(HTTPBadRequest, renderer='json')
def bad_request_view(message, request):
    """Get JSON response for a 400 status code."""
    request.response.status = 400
    return {'message': str(message), 'status': 400}


@exception_view_config(HTTPForbidden, renderer='json')
def forbidden_view(message, request):
    """Get JSON response for a 403 status code."""
    request.response.status = 403
    return {'message': str(message), 'status': 403}
