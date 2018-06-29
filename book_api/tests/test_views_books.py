"""Unit tests for the Book view functions."""

import pytest
from pyramid.httpexceptions import HTTPBadRequest, HTTPForbidden

from book_api.models.book import Book
from book_api.tests.conftest import FAKE
from book_api.views.books import _create_book


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
        _create_book(dummy_request)


def test_create_raises_error_for_incorrect_password(dummy_request, db_session, one_user):
    """Test that create raises HTTPForbidden for incorrect password."""
    db_session.add(one_user)

    data = {
        'email': one_user.email,
        'password': 'notthepassword',
        'title': FAKE.sentence(nb_words=3),
        'author': FAKE.name(),
        'isbn': FAKE.isbn13(separator="-"),
        'pub_date': FAKE.date(pattern='%m/%d/%Y')
    }
    dummy_request.POST = data
    with pytest.raises(HTTPForbidden):
        _create_book(dummy_request)


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
        _create_book(dummy_request)


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
    res = _create_book(dummy_request)
    assert isinstance(res, dict)
    assert all(prop in res for prop in
               ['id', 'title', 'author', 'isbn', 'pub_date'])


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
    _create_book(dummy_request)
    assert len(db_session.query(Book).all()) == 1


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
    res = _create_book(dummy_request)
    new_book = db_session.query(Book).get(res['id'])
    for prop in ['title', 'author', 'isbn']:
        assert getattr(new_book, prop) == data[prop]
    assert new_book.pub_date.strftime('%m/%d/%Y') == data['pub_date']


def test_create_creates_new_book_with_none_values(dummy_request, db_session, one_user):
    """Test that create sets values to None when not given."""
    db_session.add(one_user)

    data = {
        'email': one_user.email,
        'password': 'password',
        'title': FAKE.sentence(nb_words=3),
    }
    dummy_request.POST = data
    res = _create_book(dummy_request)
    assert res['author'] is None
    assert res['isbn'] is None
    assert res['pub_date'] is None
