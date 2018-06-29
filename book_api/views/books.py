"""Views for the User model."""

from datetime import datetime

from pyramid.httpexceptions import HTTPBadRequest, HTTPForbidden, HTTPNotFound
from pyramid.view import view_config
from sqlalchemy.exc import DBAPIError

from book_api.models.book import Book
from book_api.models.user import User


def validate_user(dbsession, data):
    """Validate that the request has correct email and password for an User.

    Returns the validated User object.
    """
    if not all([field in data for field in ['email', 'password']]):
        raise HTTPBadRequest

    user = dbsession.query(User).filter_by(email=data['email']).first()

    if not user or not user.verify(data['password']):
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
            pub_date: <String of mm/dd/yyyy>
        }
    'email' and 'password' are required as authentication for the user.
    The only required field is 'title'. Bad data will produce a 400 response.
    """
    data = request.GET if request.method == 'GET' else request.POST
    user = validate_user(request.dbsession, data)

    if request.method == 'GET':
        return _list_books(request, user)

    if request.method == 'POST':
        return _create_book(request, user)


@view_config(route_name='book-id', request_method=('GET', 'PUT', 'DELETE'), renderer='json')
def book_detail_update_delete_view(request):
    """Update or delete a book by ID.

    PUT request for updating a book. DELETE request for removing a book.

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
    data = request.GET if request.method == 'GET' else request.POST
    user = validate_user(request.dbsession, data)

    book_id = int(request.matchdict['id'])
    book = request.dbsession.query(Book).filter_by(user_id=user.id, id=book_id).first()

    if not book:
        raise HTTPNotFound

    if request.method == 'GET':
        return book.to_json()

    if request.method == 'PUT':
        return _update_book(request, book)

    if request.method == 'DELETE':
        return _delete_book(request, book)


def _list_books(request, user):
    """List all the books associated with a user.

    Information should be formatted as follows:
        {
            email: <String>,
            password: <String>,
        }
    'email' and 'password' are required as authentication for the user.
    """
    return [book.to_json() for book in user.books]


def _create_book(request, user):
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
    try:
        request.dbsession.flush()
    except DBAPIError:
        raise HTTPBadRequest
    request.response.status = 201
    return book.to_json()


def _update_book(request, book):
    """Update the given book with data from the request.

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
    Bad data will produce a 400 response.
    """
    if 'pub_date' in request.POST:
        try:
            request.POST['pub_date'] = datetime.strptime(request.POST['pub_date'], '%m/%d/%Y')
        except ValueError:
            raise HTTPBadRequest

    for prop in ['title', 'author', 'isbn', 'pub_date']:
        if prop in request.POST:
            setattr(book, prop, request.POST[prop])
    request.dbsession.add(book)
    try:
        request.dbsession.flush()
    except DBAPIError:
        raise HTTPBadRequest
    return book.to_json()


def _delete_book(request, book):
    """Delete the given book.

    Information should be formatted as follows:
        {
            email: <String>,
            password: <String>,
        }
    'email' and 'password' are required as authentication for the user.
    Bad data will produce a 400 response.
    """
    request.dbsession.delete(book)
    request.response.status = 204
    request.response.content_type = None
