"""Unit tests for the User model."""

import pytest
from sqlalchemy.exc import IntegrityError

from book_api.models.user import User


@pytest.fixture
def one_user():
    """Create a single User object."""
    return User(
        first_name='mo',
        last_name='person',
        email='mo@mail.com',
        password='password'
    )


def test_complete_user_model_added_to_database(db_session, one_user):
    """Test that a User can be added to the database."""
    assert len(db_session.query(User).all()) == 0
    db_session.add(one_user)
    assert len(db_session.query(User).all()) == 1


def test_incomplete_user_model_no_password_not_added_to_database(db_session):
    """Test that a User cannot be added without required fields."""
    user = User(
        first_name='mo',
        last_name='person',
        email='mo@mail.com'
    )
    db_session.add(user)
    with pytest.raises(IntegrityError):
        db_session.flush()


def test_incomplete_user_model_no_email_not_added_to_database(db_session):
    """Test that a User cannot be added without required fields."""
    user = User(
        first_name='mo',
        last_name='person',
        password='password'
    )
    db_session.add(user)
    with pytest.raises(IntegrityError):
        db_session.flush()


def test_constructed_user_model_has_hased_password(one_user):
    """Test that a User only has the hashed version of the password."""
    assert one_user.password != 'password'


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
