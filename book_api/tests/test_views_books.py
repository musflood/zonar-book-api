"""Unit tests for the Book view functions."""

import pytest
from pyramid.httpexceptions import HTTPBadRequest, HTTPForbidden

from book_api.models.book import Book
from book_api.tests.conftest import FAKE
from book_api.views.books import (
    _create_book, _delete_book, _list_books, _update_book, validate_user)


def test_validate_user_raises_error_for_incomplete_data(dummy_request):
    """Test that validate_user raises HTTPBadRequest for missing password."""
    data = {
        'email': FAKE.email()
    }
    with pytest.raises(HTTPBadRequest):
        validate_user(dummy_request.dbsession, data)


def test_validate_user_raises_error_for_email_not_in_database(dummy_request):
    """Test that validate_user raises HTTPForbidden for bad email."""
    data = {
        'email': FAKE.email(),
        'password': 'password'
    }
    with pytest.raises(HTTPForbidden):
        validate_user(dummy_request.dbsession, data)


def test_validate_user_raises_error_for_incorrect_password(dummy_request, db_session, one_user):
    """Test that validate_user raises HTTPForbidden for bad email."""
    db_session.add(one_user)

    data = {
        'email': one_user.email,
        'password': 'notthepassword'
    }
    with pytest.raises(HTTPForbidden):
        validate_user(dummy_request.dbsession, data)


def test_validate_user_returns_user_matching_email(dummy_request, db_session, one_user):
    """Test that validate_user raises HTTPForbidden for bad email."""
    db_session.add(one_user)

    data = {
        'email': one_user.email,
        'password': 'password'
    }
    auth_user = validate_user(dummy_request.dbsession, data)
    assert auth_user is one_user


def test_list_empty_for_user_with_no_books(dummy_request, db_session, one_user):
    """Test that list returns empty list for user with no books."""
    db_session.add(one_user)

    data = {
        'email': one_user.email,
        'password': 'password',
    }
    dummy_request.GET = data
    books = _list_books(dummy_request, one_user)
    assert books == []


def test_create_raises_error_for_incomplete_post_data(dummy_request, db_session, one_user):
    """Test that create raises HTTPBadRequest for missing title."""
    db_session.add(one_user)

    data = {
        'email': one_user.email,
        'password': 'password',
        'author': FAKE.name(),
        'isbn': FAKE.isbn13(separator="-"),
        'pub_date': FAKE.date(pattern='%m/%d/%Y')
    }
    dummy_request.POST = data
    with pytest.raises(HTTPBadRequest):
        _create_book(dummy_request, one_user)


def test_create_raises_error_for_bad_date_format(dummy_request, db_session, one_user):
    """Test that create raises HTTPBadRequest for incorrect date format."""
    db_session.add(one_user)

    data = {
        'email': one_user.email,
        'password': 'password',
        'title': FAKE.sentence(nb_words=3),
        'author': FAKE.name(),
        'isbn': FAKE.isbn13(separator="-"),
        'pub_date': FAKE.date(pattern='%Y-%m-%d')
    }
    dummy_request.POST = data
    with pytest.raises(HTTPBadRequest):
        _create_book(dummy_request, one_user)


def test_create_adds_new_book_to_the_database(dummy_request, db_session, one_user):
    """Test that create adds a new Book to the database."""
    db_session.add(one_user)

    assert len(db_session.query(Book).all()) == 0
    data = {
        'email': one_user.email,
        'password': 'password',
        'title': FAKE.sentence(nb_words=3),
        'author': FAKE.name(),
        'isbn': FAKE.isbn13(separator="-"),
        'pub_date': FAKE.date(pattern='%m/%d/%Y')
    }
    dummy_request.POST = data
    _create_book(dummy_request, one_user)
    assert len(db_session.query(Book).all()) == 1


def test_create_returns_dict_with_new_book_data(dummy_request, db_session, one_user):
    """Test that create returns dict with the new Book's data."""
    db_session.add(one_user)

    data = {
        'email': one_user.email,
        'password': 'password',
        'title': FAKE.sentence(nb_words=3),
        'author': FAKE.name(),
        'isbn': FAKE.isbn13(separator="-"),
        'pub_date': FAKE.date(pattern='%m/%d/%Y')
    }
    dummy_request.POST = data
    res = _create_book(dummy_request, one_user)
    assert isinstance(res, dict)
    assert all(prop in res for prop in
               ['id', 'title', 'author', 'isbn', 'pub_date'])


def test_create_creates_new_book_using_post_data(dummy_request, db_session, one_user):
    """Test that create uses POST data to create the new Book."""
    db_session.add(one_user)

    data = {
        'email': one_user.email,
        'password': 'password',
        'title': FAKE.sentence(nb_words=3),
        'author': FAKE.name(),
        'isbn': FAKE.isbn13(separator="-"),
        'pub_date': FAKE.date(pattern='%m/%d/%Y')
    }
    dummy_request.POST = data
    res = _create_book(dummy_request, one_user)
    new_book = db_session.query(Book).get(res['id'])
    for prop in ['title', 'author', 'isbn']:
        assert getattr(new_book, prop) == data[prop]
    assert new_book.pub_date.strftime('%m/%d/%Y') == data['pub_date']


def test_create_sets_email_user_as_owner_of_new_book(dummy_request, db_session, one_user):
    """Test that create uses email from POST data to set Book owner."""
    db_session.add(one_user)

    data = {
        'email': one_user.email,
        'password': 'password',
        'title': FAKE.sentence(nb_words=3),
        'author': FAKE.name(),
        'isbn': FAKE.isbn13(separator="-"),
        'pub_date': FAKE.date(pattern='%m/%d/%Y')
    }
    dummy_request.POST = data
    res = _create_book(dummy_request, one_user)
    new_book = db_session.query(Book).get(res['id'])
    assert one_user is new_book.user


def test_create_creates_new_book_with_none_values(dummy_request, db_session, one_user):
    """Test that create sets values to None when not given."""
    db_session.add(one_user)

    data = {
        'email': one_user.email,
        'password': 'password',
        'title': FAKE.sentence(nb_words=3),
    }
    dummy_request.POST = data
    res = _create_book(dummy_request, one_user)
    assert res['author'] is None
    assert res['isbn'] is None
    assert res['pub_date'] is None


def test_list_has_all_books_for_user(dummy_request, db_session, one_user):
    """Test that list returns filled list for user with multiple books."""
    db_session.add(one_user)

    data = {
        'email': one_user.email,
        'password': 'password',
    }
    dummy_request.GET = data
    books = _list_books(dummy_request, one_user)
    assert len(books) == len(one_user.books)


def test_list_returns_list_of_dict_with_book_data(dummy_request, db_session, one_user):
    """Test that list returns list of dict with the user Book data."""
    db_session.add(one_user)

    data = {
        'email': one_user.email,
        'password': 'password',
    }
    dummy_request.GET = data
    res = _list_books(dummy_request, one_user)
    for book in res:
        assert all(prop in book for prop in
                   ['id', 'title', 'author', 'isbn', 'pub_date'])


def test_update_raises_error_for_bad_date_format(dummy_request, db_session, one_user):
    """Test that update raises HTTPBadRequest for incorrect date format."""
    db_session.add(one_user)
    book = db_session.query(Book).first()

    data = {
        'email': one_user.email,
        'password': 'password',
        'pub_date': FAKE.date(pattern='%Y-%m-%d')
    }
    dummy_request.POST = data
    with pytest.raises(HTTPBadRequest):
        _update_book(dummy_request, book)


def test_update_changes_single_value_for_given_book_using_post_data(dummy_request, db_session, one_user):
    """Test that update changes the values on the given book from POST data."""
    db_session.add(one_user)
    book = db_session.query(Book).first()

    new_author = FAKE.name()
    assert new_author != book.author

    data = {
        'email': one_user.email,
        'password': 'password',
        'author': new_author
    }
    dummy_request.POST = data
    _update_book(dummy_request, book)
    assert book.author == new_author


def test_update_changes_all_values_for_given_book_using_post_data(dummy_request, db_session, one_user):
    """Test that update changes the values on the given book from POST data."""
    db_session.add(one_user)
    book = db_session.query(Book).first()

    data = {
        'email': one_user.email,
        'password': 'password',
        'title': FAKE.sentence(nb_words=3),
        'author': FAKE.name(),
        'isbn': FAKE.isbn13(separator="-"),
        'pub_date': FAKE.date(pattern='%m/%d/%Y')
    }
    for prop in ['title', 'author', 'isbn', 'pub_date']:
        assert getattr(book, prop) != data[prop]

    dummy_request.POST = data
    _update_book(dummy_request, book)

    for prop in ['title', 'author', 'isbn', 'pub_date']:
        assert getattr(book, prop) == data[prop]


def test_update_returns_dict_with_updated_book_data(dummy_request, db_session, one_user):
    """Test that update returns dict with the new Book's data."""
    db_session.add(one_user)
    book = db_session.query(Book).first()

    data = {
        'email': one_user.email,
        'password': 'password',
        'title': FAKE.sentence(nb_words=3),
        'author': FAKE.name(),
        'isbn': FAKE.isbn13(separator="-"),
        'pub_date': FAKE.date(pattern='%m/%d/%Y')
    }
    dummy_request.POST = data
    res = _update_book(dummy_request, book)
    assert isinstance(res, dict)
    assert all(prop in res for prop in
               ['id', 'title', 'author', 'isbn', 'pub_date'])


def test_delete_returns_nothing(dummy_request, db_session, one_user):
    """Test that delete returns None."""
    db_session.add(one_user)
    book = db_session.query(Book).first()

    data = {
        'email': one_user.email,
        'password': 'password',
    }
    dummy_request.POST = data
    res = _delete_book(dummy_request, book)
    assert res is None


def test_delete_removes_book_from_database(dummy_request, db_session, one_user):
    """Test that delete removes the given book from the database."""
    db_session.add(one_user)
    book = db_session.query(Book).first()
    book_id = book.id

    data = {
        'email': one_user.email,
        'password': 'password',
    }
    dummy_request.POST = data
    _delete_book(dummy_request, book)
    db_session.commit()
    assert db_session.query(Book).get(book_id) is None
