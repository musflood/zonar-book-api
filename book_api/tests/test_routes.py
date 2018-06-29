"""Functional tests for all the routes."""

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
