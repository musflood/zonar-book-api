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


def test_book_list_get_missing_auth_gets_400_status_code(testapp, testapp_session, one_user, fill_the_db):
    """Test that GET to book-list route gets 400 status code for missing auth."""
    testapp_session.add(one_user)
    testapp_session.commit()

    res = testapp.get('/books', status=400)
    assert res.status_code == 400


def test_book_list_get_incorrect_auth_gets_403_status_code(testapp, one_user):
    """Test that GET to book-list route gets 403 status code for bad auth."""
    data = {
        'email': one_user.email,
        'password': 'notthepassword',
    }
    res = testapp.get('/books', data, status=403)
    assert res.status_code == 403


def test_book_list_get_correct_auth_has_200_response_code(testapp, one_user):
    """Test that GET to book-list route gets 200 status code for good auth."""
    data = {
        'email': one_user.email,
        'password': 'password',
    }
    res = testapp.get('/books', data)
    assert res.status_code == 200


def test_book_list_get_correct_auth_empty_for_user_with_no_books(testapp, one_user):
    """Test that GET to book-list route returns empty list for user without books."""
    data = {
        'email': one_user.email,
        'password': 'password',
    }
    res = testapp.get('/books', data)
    assert res.json == []


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


def test_book_list_post_incorrect_auth_gets_403_status_code(testapp, one_user):
    """Test that POST to book-list route gets 403 status code for bad auth."""
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


def test_book_list_post_incorrect_date_gets_400_status_code(testapp, one_user):
    """Test that POST to book-list route gets 400 status code for bad data."""
    data = {
        'email': one_user.email,
        'password': 'password',
        'title': FAKE.sentence(nb_words=3),
        'author': FAKE.name(),
        'isbn': FAKE.isbn13(separator="-"),
        'pub_date': FAKE.date(pattern='%Y-%m-%d')
    }
    res = testapp.post('/books', data, status=400)
    assert res.status_code == 400


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


def test_book_list_post_complete_data_adds_book_to_database(testapp, testapp_session, one_user):
    """Test that POST to book-list route creates a new Book."""
    num_books = len(testapp_session.query(Book).all())
    data = {
        'email': one_user.email,
        'password': 'password',
        'title': FAKE.sentence(nb_words=3),
        'author': FAKE.name(),
        'isbn': FAKE.isbn13(separator="-"),
        'pub_date': FAKE.date(pattern='%m/%d/%Y')
    }
    testapp.post('/books', data)
    assert len(testapp_session.query(Book).all()) == num_books + 1


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


def test_book_list_post_complete_data_returns_json_with_new_book_info(testapp, one_user):
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


def test_book_list_post_data_without_values_sets_values_to_none(testapp, one_user):
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


def test_book_list_get_correct_auth_all_books_for_user(testapp, testapp_session, one_user):
    """Test that GET to book-list route lists all books for the users."""
    data = {
        'email': one_user.email,
        'password': 'password',
    }
    res = testapp.get('/books', data)
    user_books = testapp_session.query(User).get(one_user.id).books
    assert len(res.json) == len(user_books)


def test_book_list_get_correct_auth_all_book_details(testapp, one_user):
    """Test that GET to book-list route has details for every book."""
    data = {
        'email': one_user.email,
        'password': 'password',
    }
    res = testapp.get('/books', data)
    for book in res.json:
        assert all(prop in book for prop in
                   ['id', 'title', 'author', 'isbn', 'pub_date'])


def test_book_id_other_methods_gets_404_status_code(testapp):
    """Test that other HTTP method requests to book-id get a 404 status code."""
    for method in ('post',):
        res = getattr(testapp, method)('/books/1', status=404)
        assert res.status_code == 404


def test_book_id_get_missing_auth_gets_400_status_code(testapp, testapp_session, one_user):
    """Test that GET to book-id route gets 400 status code for missing auth."""
    res = testapp.get('/books/1', status=400)
    assert res.status_code == 400


def test_book_id_get_incorrect_auth_gets_403_status_code(testapp, one_user):
    """Test that GET to book-id route gets 403 status code for bad auth."""
    data = {
        'email': one_user.email,
        'password': 'notthepassword',
    }
    res = testapp.get('/books/1', data, status=403)
    assert res.status_code == 403


def test_book_id_get_correct_auth_not_users_book_gets_404_status_code(testapp, testapp_session, one_user):
    """Test that GET to book-id route gets 404 status code for book that does not beling to user."""
    book = testapp_session.query(Book).filter(Book.user_id != one_user.id).first()

    data = {
        'email': one_user.email,
        'password': 'password',
    }
    res = testapp.get('/books/{}'.format(book.id), data, status=404)
    assert res.status_code == 404


def test_book_id_get_correct_auth_has_200_response_code(testapp, testapp_session, one_user):
    """Test that GET to book-id route gets 200 status code for good auth."""
    book = testapp_session.query(User).get(one_user.id).books[0]

    data = {
        'email': one_user.email,
        'password': 'password',
    }
    res = testapp.get('/books/{}'.format(book.id), data)
    assert res.status_code == 200


def test_book_id_get_correct_auth_returns_json_with_book_info(testapp, testapp_session, one_user):
    """Test that GET to book-id route gets 200 status code for good auth."""
    book = testapp_session.query(User).get(one_user.id).books[0]

    data = {
        'email': one_user.email,
        'password': 'password',
    }
    res = testapp.get('/books/{}'.format(book.id), data)
    for prop in ['id', 'title', 'author', 'isbn']:
        assert res.json[prop] == getattr(book, prop)
    assert res.json['pub_date'] == book.pub_date.strftime('%m/%d/%Y')


def test_book_id_put_missing_auth_gets_400_status_code(testapp, testapp_session, one_user):
    """Test that PUT to book-id route gets 400 status code for missing auth."""
    res = testapp.put('/books/1', status=400)
    assert res.status_code == 400


def test_book_id_put_incorrect_auth_gets_403_status_code(testapp, one_user):
    """Test that PUT to book-id route gets 403 status code for bad auth."""
    data = {
        'email': one_user.email,
        'password': 'notthepassword',
    }
    res = testapp.put('/books/1', data, status=403)
    assert res.status_code == 403


def test_book_id_put_correct_auth_not_users_book_gets_404_status_code(testapp, testapp_session, one_user):
    """Test that PUT to book-id route gets 404 status code for book that does not beling to user."""
    book = testapp_session.query(Book).filter(Book.user_id != one_user.id).first()

    data = {
        'email': one_user.email,
        'password': 'password',
    }
    res = testapp.put('/books/{}'.format(book.id), data, status=404)
    assert res.status_code == 404


def test_book_id_put_correct_auth_incorrect_date_gets_400_status_code(testapp, testapp_session, one_user):
    """Test that POST to book-id route gets 400 status code for bad data."""
    book = testapp_session.query(User).get(one_user.id).books[0]

    data = {
        'email': one_user.email,
        'password': 'password',
        'pub_date': FAKE.date(pattern='%Y-%m-%d')
    }
    res = testapp.put('/books/{}'.format(book.id), data, status=400)
    assert res.status_code == 400


def test_book_id_put_correct_auth_has_200_response_code(testapp, testapp_session, one_user):
    """Test that PUT to book-id route gets 200 status code for good auth."""
    book = testapp_session.query(User).get(one_user.id).books[0]

    data = {
        'email': one_user.email,
        'password': 'password',
        'author': FAKE.name()
    }
    res = testapp.put('/books/{}'.format(book.id), data)
    assert res.status_code == 200


def test_book_id_put_correct_auth_does_not_add_book_to_database(testapp, testapp_session, one_user):
    """Test that PUT to book-id route does not create a new Book."""
    book = testapp_session.query(User).get(one_user.id).books[0]

    num_books = len(testapp_session.query(Book).all())
    data = {
        'email': one_user.email,
        'password': 'password',
        'isbn': FAKE.isbn13(separator="-")
    }
    testapp.put('/books/{}'.format(book.id), data)
    assert len(testapp_session.query(Book).all()) == num_books


def test_book_id_put_correct_auth_updates_book_in_database(testapp, testapp_session, one_user):
    """Test that PUT to book-id route gets 200 status code for good auth."""
    book = testapp_session.query(User).get(one_user.id).books[0]

    data = {
        'email': one_user.email,
        'password': 'password',
        'author': FAKE.name()
    }
    testapp.put('/books/{}'.format(book.id), data)

    updated_book = testapp.get('/books/{}'.format(book.id), data)
    assert updated_book.json['author'] == data['author']


def test_book_id_put_correct_auth_returns_json_with_updated_book_info(testapp, testapp_session, one_user):
    """Test that PUT to book-id route gets 200 status code for good auth."""
    book = testapp_session.query(User).get(one_user.id).books[0]

    data = {
        'email': one_user.email,
        'password': 'password',
        'author': FAKE.name(),
        'isbn': FAKE.isbn13(separator="-"),
        'pub_date': FAKE.date(pattern='%m/%d/%Y')
    }
    res = testapp.put('/books/{}'.format(book.id), data)

    for prop in ['id', 'title', 'author', 'isbn', 'pub_date']:
        if prop in data:
            assert res.json[prop] == data[prop]
        else:
            assert res.json[prop] == getattr(book, prop)
