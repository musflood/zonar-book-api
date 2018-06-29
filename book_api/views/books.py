"""Views for the User model."""

from datetime import datetime

from pyramid.httpexceptions import HTTPBadRequest, HTTPForbidden
from pyramid.view import view_config

from book_api.models.book import Book
from book_api.models.user import User


def validate_user(request):
    """Validate that the request has correct email and password for an User.

    Returns the validated User object.
    """
    if not all([field in request.POST for field in ['email', 'password']]):
        raise HTTPBadRequest

    user = request.dbsession.query(User).filter_by(email=request.POST['email']).first()

    if not user or not user.verify(request.POST['password']):
        raise HTTPForbidden('The given email and password do not match.')

    return user


@view_config(route_name='book-list', request_method=('GET', 'POST'), renderer='json')
def book_list_create_view(request):
    """List the books for a user or add a new book to the list.

    GET request for listing books. POST request for adding new book.

    Information should be formatted as follows:
        {
            email: <String>,
            password: <String>,

            title: <String>,
            author: <String>,
            isbn: <String>,
            pub_date: <String>
        }
    'email' and 'password' are required as authentication for the user.
    The only required field is 'title'. Bad data will produce a 400 response.
    """
    if request.method == 'POST':
        _create_book(request)


def _create_book(request):
    """Add a new book to the wish list of a user.

    Information should be formatted as follows:
        {
            email: <String>,
            password: <String>,

            title: <String>,
            author: <String>,
            isbn: <String>,
            pub_date: <String of mm/dd/yyyy>
        }
    'email' and 'password' are required as authentication for the user.
    The only required field is 'title'. Bad data will produce a 400 response.
    """
    user = validate_user(request)

    if 'title' not in request.POST:
        raise HTTPBadRequest

    if 'pub_date' in request.POST:
        try:
            pub_date = datetime.strptime(request.POST['pub_date'], '%m/%d/%Y')
        except ValueError:
            raise HTTPBadRequest

    book = Book(
        user=user,
        title=request.POST['title'],
        author=request.POST['author'] if 'author' in request.POST else None,
        isbn=request.POST['isbn'] if 'isbn' in request.POST else None,
        pub_date=pub_date if 'pub_date' in request.POST else None,
    )
    request.dbsession.add(book)
    request.dbsession.flush()
    request.response.status = 201
    return book.to_json()
