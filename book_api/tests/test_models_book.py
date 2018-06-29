"""Unit tests for the Book model."""

import pytest
from sqlalchemy.exc import IntegrityError

from book_api.models.book import Book
from book_api.models.user import User
from book_api.tests.conftest import FAKE


def test_complete_book_added_to_database(db_session, one_book):
    """Test that a Book is added to the database when user is set."""
    assert len(db_session.query(Book).all()) == 0
    db_session.add(one_book)
    assert len(db_session.query(Book).all()) == 1


def test_incomplete_book_no_user_not_added_to_database(db_session):
    """Test that a Book cannot be added without required fields."""
    book = Book(
        title=FAKE.sentence(nb_words=3),
        author=FAKE.name(),
        isbn=FAKE.isbn13(separator="-"),
        pub_date=FAKE.date_object()
    )
    db_session.add(book)
    with pytest.raises(IntegrityError):
        db_session.flush()


def test_incomplete_book_no_title_not_added_to_database(db_session, one_user):
    """Test that a Book cannot be added without required fields."""
    book = Book(
        user=one_user,
        author=FAKE.name(),
        isbn=FAKE.isbn13(separator="-"),
        pub_date=FAKE.date_object()
    )
    db_session.add(book)
    with pytest.raises(IntegrityError):
        db_session.flush()


def test_book_has_access_to_parent_user_model(one_book, one_user):
    """Test that a Book has access to the parent User and its properties."""
    assert isinstance(one_book.user, User)
    assert one_book.user.email == one_user.email


def test_to_json_has_all_book_properties_except_user(one_book):
    """Test that to_json has all the properties on the Book model."""
    json = one_book.to_json()
    assert all(prop in json for prop in
               ['id', 'title', 'author', 'isbn', 'pub_date'])


def test_to_json_has_property_values_from_object(one_book):
    """Test that to_json has the correct values from the Book."""
    json = one_book.to_json()
    for prop in ['id', 'title', 'author', 'isbn']:
        assert json[prop] == getattr(one_book, prop)
    assert json['pub_date'] == one_book.pub_date.strftime('%m/%d/%Y')
