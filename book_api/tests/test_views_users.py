"""Unit tests for the User view functions."""

import pytest
from pyramid.httpexceptions import HTTPBadRequest

from book_api.models.user import User
from book_api.tests.conftest import FAKE
from book_api.views.users import signup_view


def test_signup_raises_error_for_incomplete_post_data(dummy_request):
    """Test that signup raises HTTPBadRequest for missing email."""
    data = {
        'first_name': FAKE.first_name(),
        'last_name': FAKE.last_name(),
        'password': FAKE.password()
    }
    dummy_request.POST = data
    with pytest.raises(HTTPBadRequest):
        signup_view(dummy_request)


def test_signup_raises_error_for_duplicate_email(dummy_request, db_session, one_user):
    """Test that signup raises HTTPBadRequest for duplicate email."""
    db_session.add(one_user)
    data = {
        'first_name': FAKE.first_name(),
        'last_name': FAKE.last_name(),
        'email': one_user.email,
        'password': FAKE.password()
    }
    dummy_request.POST = data
    with pytest.raises(HTTPBadRequest):
        signup_view(dummy_request)


def test_signup_returns_dict_with_new_user_data(dummy_request):
    """Test that signup returns dict with the new User's data."""
    data = {
        'first_name': FAKE.first_name(),
        'last_name': FAKE.last_name(),
        'email': FAKE.email(),
        'password': FAKE.password()
    }
    dummy_request.POST = data
    res = signup_view(dummy_request)
    assert isinstance(res, dict)
    assert all(prop in res for prop in
               ['id', 'first_name', 'last_name', 'email'])


def test_signup_adds_new_user_to_the_database(dummy_request, db_session):
    """Test that signup adds a new User to the database."""
    data = {
        'first_name': FAKE.first_name(),
        'last_name': FAKE.last_name(),
        'email': FAKE.email(),
        'password': FAKE.password()
    }
    dummy_request.POST = data
    signup_view(dummy_request)
    assert len(db_session.query(User).all()) == 1


def test_signup_creates_new_user_using_post_data(dummy_request, db_session):
    """Test that signup uses POST data to create the new User."""
    data = {
        'first_name': FAKE.first_name(),
        'last_name': FAKE.last_name(),
        'email': FAKE.email(),
        'password': FAKE.password()
    }
    dummy_request.POST = data
    res = signup_view(dummy_request)
    new_user = db_session.query(User).get(res['id'])
    for prop in ['first_name', 'last_name', 'email']:
        assert getattr(new_user, prop) == data[prop]
    assert new_user.verify(data['password'])
