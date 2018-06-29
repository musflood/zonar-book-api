"""Functional tests for all the routes."""

from book_api.models.book import Book
from book_api.models.user import User
from book_api.tests.conftest import FAKE


def test_signup_other_methods_gets_404_status_code(testapp):
    """Test that other HTTP method requests to signup get a 404 status code."""
    for method in ('get', 'put', 'delete'):
        res = getattr(testapp, method)('/signup', status=404)
        assert res.status_code == 404


def test_signup_post_no_data_gets_400_status_code(testapp):
    """Test that POST to signup route gets 400 status code with no data."""
    res = testapp.post('/signup', status=400)
    assert res.status_code == 400


def test_signup_post_incomplete_data_gets_400_status_code(testapp):
    """Test that POST to signup route gets 400 status code for bad data."""
    data = {
        'first_name': FAKE.first_name(),
        'last_name': FAKE.last_name(),
        'password': FAKE.password()
    }
    res = testapp.post('/signup', data, status=400)
    assert res.status_code == 400


def test_signup_post_complete_data_adds_user_to_database(testapp, testapp_session):
    """Test that POST to signup route creates a new User."""
    assert len(testapp_session.query(User).all()) == 0
    data = {
        'first_name': FAKE.first_name(),
        'last_name': FAKE.last_name(),
        'email': FAKE.email(),
        'password': FAKE.password()
    }
    testapp.post('/signup', data)
    assert len(testapp_session.query(User).all()) == 1


def test_signup_post_complete_data_gets_201_status_code(testapp):
    """Test that POST to signup route gets 201 status code."""
    data = {
        'first_name': FAKE.first_name(),
        'last_name': FAKE.last_name(),
        'email': FAKE.email(),
        'password': FAKE.password()
    }
    res = testapp.post('/signup', data)
    assert res.status_code == 201


def test_signup_post_complete_data_returns_json_with_new_user_info(testapp):
    """Test that POST to signup route gets JSON with details for new User."""
    data = {
        'first_name': FAKE.first_name(),
        'last_name': FAKE.last_name(),
        'email': FAKE.email(),
        'password': FAKE.password()
    }
    res = testapp.post('/signup', data)
    for prop in ['first_name', 'last_name', 'email']:
        assert res.json[prop] == data[prop]
    assert res.json['id'] is not None


def test_signup_post_data_without_names_sets_names_to_none(testapp):
    """Test that POST to signup route sets first and last names to None."""
    data = {
        'email': FAKE.email(),
        'password': FAKE.password()
    }
    res = testapp.post('/signup', data)
    assert res.json['first_name'] is None
    assert res.json['last_name'] is None


def test_book_list_other_methods_gets_404_status_code(testapp):
    """Test that other HTTP method requests to book-list get a 404 status code."""
    for method in ('put', 'delete'):
        res = getattr(testapp, method)('/books', status=404)
        assert res.status_code == 404


def test_book_list_post_no_data_gets_400_status_code(testapp):
    """Test that POST to book-list route gets 400 status code with no data."""
    res = testapp.post('/books', status=400)
    assert res.status_code == 400


def test_book_list_post_missing_auth_gets_400_status_code(testapp):
    """Test that POST to book-list route gets 400 status code for missing auth."""
    data = {
        'title': FAKE.sentence(nb_words=3),
        'author': FAKE.name(),
        'isbn': FAKE.isbn13(separator="-"),
        'pub_date': FAKE.date(pattern='%m/%d/%Y')
    }
    res = testapp.post('/books', data, status=400)
    assert res.status_code == 400


def test_book_list_post_incorrect_auth_gets_403_status_code(testapp, testapp_session, one_user):
    """Test that POST to book-list route gets 403 status code for bad auth."""
    testapp_session.add(one_user)
    testapp_session.commit()

    data = {
        'email': one_user.email,
        'password': 'notthepassword',
        'title': FAKE.sentence(nb_words=3),
        'author': FAKE.name(),
        'isbn': FAKE.isbn13(separator="-"),
        'pub_date': FAKE.date(pattern='%m/%d/%Y')
    }
    res = testapp.post('/books', data, status=403)
    assert res.status_code == 403


def test_book_list_post_incomplete_data_gets_400_status_code(testapp, one_user):
    """Test that POST to book-list route gets 400 status code for missing data."""
    data = {
        'email': one_user.email,
        'password': 'password',
        'author': FAKE.name(),
        'isbn': FAKE.isbn13(separator="-"),
        'pub_date': FAKE.date(pattern='%m/%d/%Y')
    }
    res = testapp.post('/books', data, status=400)
    assert res.status_code == 400


def test_book_list_post_complete_data_adds_book_to_database(testapp, testapp_session, one_user):
    """Test that POST to book-list route creates a new Book."""
    assert len(testapp_session.query(Book).all()) == 0
    data = {
        'email': one_user.email,
        'password': 'password',
        'title': FAKE.sentence(nb_words=3),
        'author': FAKE.name(),
        'isbn': FAKE.isbn13(separator="-"),
        'pub_date': FAKE.date(pattern='%m/%d/%Y')
    }
    testapp.post('/books', data)
    assert len(testapp_session.query(Book).all()) == 1


def test_book_list_post_sets_email_user_as_book_owner(testapp, testapp_session, one_user):
    """Test that POST to book-list route sets user with email as book owner."""
    data = {
        'email': one_user.email,
        'password': 'password',
        'title': FAKE.sentence(nb_words=3),
        'author': FAKE.name(),
        'isbn': FAKE.isbn13(separator="-"),
        'pub_date': FAKE.date(pattern='%m/%d/%Y')
    }
    res = testapp.post('/books', data)
    new_book = testapp_session.query(Book).get(res.json['id'])
    assert new_book.user.email == one_user.email


def test_book_list_post_complete_data_gets_201_status_code(testapp, one_user):
    """Test that POST to book-list route gets 201 status code."""
    data = {
        'email': one_user.email,
        'password': 'password',
        'title': FAKE.sentence(nb_words=3),
        'author': FAKE.name(),
        'isbn': FAKE.isbn13(separator="-"),
        'pub_date': FAKE.date(pattern='%m/%d/%Y')
    }
    res = testapp.post('/books', data)
    assert res.status_code == 201


def test_book_list_post_complete_data_returns_json_with_new_user_info(testapp, one_user):
    """Test that POST to book-list route gets JSON with details for new Book."""
    data = {
        'email': one_user.email,
        'password': 'password',
        'title': FAKE.sentence(nb_words=3),
        'author': FAKE.name(),
        'isbn': FAKE.isbn13(separator="-"),
        'pub_date': FAKE.date(pattern='%m/%d/%Y')
    }
    res = testapp.post('/books', data)
    for prop in ['title', 'author', 'isbn', 'pub_date']:
        assert res.json[prop] == data[prop]
    assert res.json['id'] is not None


def test_book_list_post_data_without_names_sets_names_to_none(testapp, one_user):
    """Test that POST to book-list route sets first and last names to None."""
    data = {
        'email': one_user.email,
        'password': 'password',
        'title': FAKE.sentence(nb_words=3),
    }
    res = testapp.post('/books', data)
    assert res.json['author'] is None
    assert res.json['isbn'] is None
    assert res.json['pub_date'] is None
