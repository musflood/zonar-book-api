"""Fixtures for the book_api tests."""

import os

from faker import Faker
from pyramid import testing
import pytest

from book_api.models.book import Book
from book_api.models.meta import Base
from book_api.models.user import User

BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)

TEST_DATABASE = 'sqlite:///{}/test_book_api.sqlite'.format(BASE_DIR)

FAKE = Faker()


@pytest.fixture(scope='session')
def configuration(request):
    """Set up a database for testing purposes."""
    config = testing.setUp(settings={
        'sqlalchemy.url': TEST_DATABASE
    })
    config.include('book_api.models')
    config.include("book_api.routes")

    def teardown():
        testing.tearDown()

    request.addfinalizer(teardown)
    return config


@pytest.fixture
def db_session(configuration, request):
    """Create a database session for interacting with the test database."""
    SessionFactory = configuration.registry['dbsession_factory']
    session = SessionFactory()
    engine = session.bind
    Base.metadata.create_all(engine)

    def teardown():
        session.transaction.rollback()
        Base.metadata.drop_all(engine)

    request.addfinalizer(teardown)
    return session


@pytest.fixture
def dummy_request(db_session):
    """Create a dummy GET request with a dbsession."""
    return testing.DummyRequest(dbsession=db_session)


@pytest.fixture(scope="session")
def testapp(request):
    """Functional test for app."""
    from webtest import TestApp
    from book_api import main

    app = main({}, **{'sqlalchemy.url': TEST_DATABASE})

    SessionFactory = app.registry["dbsession_factory"]
    engine = SessionFactory().bind
    Base.metadata.create_all(bind=engine)

    def tearDown():
        Base.metadata.drop_all(bind=engine)

    request.addfinalizer(tearDown)

    return TestApp(app)


# Model fixtures #

@pytest.fixture(scope='module')
def one_user():
    """Create a single User object."""
    return User(
        first_name=FAKE.first_name(),
        last_name=FAKE.last_name(),
        email=FAKE.email(),
        password='password'
    )


@pytest.fixture
def one_book(one_user):
    """Create a single Book object."""
    return Book(
        user=one_user,
        title=FAKE.sentence(nb_words=3),
        author=FAKE.name(),
        isbn=FAKE.isbn13(separator="-"),
        pub_date=FAKE.date_object()
    )
