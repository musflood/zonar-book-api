"""Unit tests for the User model."""

import pytest
from sqlalchemy.exc import IntegrityError

from book_api.models.user import User


@pytest.fixture(scope='module')
def one_user():
    """Create a single User object."""
    return User(
        first_name='Mo',
        last_name='Person',
        email='mo@mail.com',
        password='password'
    )


def test_complete_user_added_to_database(db_session, one_user):
    """Test that a User can be added to the database."""
    assert len(db_session.query(User).all()) == 0
    db_session.add(one_user)
    assert len(db_session.query(User).all()) == 1


def test_incomplete_user_no_password_not_added_to_database(db_session):
    """Test that a User cannot be added without required fields."""
    user = User(
        first_name='Mo',
        last_name='Person',
        email='mo@mail.com'
    )
    db_session.add(user)
    with pytest.raises(IntegrityError):
        db_session.flush()


def test_incomplete_user_no_email_not_added_to_database(db_session):
    """Test that a User cannot be added without required fields."""
    user = User(
        first_name='Mo',
        last_name='pPerson',
        password='password'
    )
    db_session.add(user)
    with pytest.raises(IntegrityError):
        db_session.flush()


def test_user_duplicate_email_not_added_to_database(db_session, one_user):
    """Test that a User can be added to the database."""
    db_session.add(one_user)
    db_session.flush()
    dup_user = User(
        first_name='Bob',
        last_name='Friend',
        email='mo@mail.com',
        password='supersecret'
    )
    db_session.add(dup_user)
    with pytest.raises(IntegrityError):
        db_session.flush()


def test_constructed_user_has_hased_password(one_user):
    """Test that a User only has the hashed version of the password."""
    assert one_user.password != 'password'


def test_user_with_no_books_has_access_to_books_list(one_user):
    """Test that a User has access to a list of their books."""
    assert isinstance(one_user.books, list)
    assert len(one_user.books) == 0


def test_verify_returns_true_for_correct_password(one_user):
    """Test that verify method returns True for the correct password."""
    assert one_user.verify('password') is True


def test_verify_returns_false_for_incorrect_password(one_user):
    """Test that verify method returns False for an incorrect password."""
    assert one_user.verify('notthepassword') is False


def test_to_json_has_all_user_properties_except_password(one_user):
    """Test that to_json has all the properties on the User model."""
    json = one_user.to_json()
    assert all(prop in json for prop in
               ['id', 'first_name', 'last_name', 'email'])


def test_to_json_has_property_values_from_object(one_user):
    """Test that to_json has the correct values from the User."""
    json = one_user.to_json()
    for prop in ['id', 'first_name', 'last_name', 'email']:
        assert json[prop] == getattr(one_user, prop)
