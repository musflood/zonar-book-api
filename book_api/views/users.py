"""Views for the User model."""

from pyramid.httpexceptions import HTTPBadRequest
from pyramid.view import view_config
from sqlalchemy.exc import DBAPIError

from book_api.models.user import User


@view_config(route_name='signup', request_method='POST', renderer='json')
def signup_view(request):
    """Create a new User from given information.

    Only accepts POST requests.

    Information should be formatted as follows:
        {
            first_name: <String>,
            last_name: <String>,
            email: <String>,
            password: <String>
        }
    The only required fields are 'email' and 'password' and 'email' must be
    unique. Bad data will produce a 400 response.
    """
    if not all([field in request.POST for field in ['email', 'password']]):
        raise HTTPBadRequest
    user = User(**request.POST)
    request.dbsession.add(user)
    try:
        request.dbsession.flush()
    except DBAPIError:
        raise HTTPBadRequest('A User with that email already exits.')
    request.response.status = 201
    return user.to_json()
