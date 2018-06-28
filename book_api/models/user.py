"""Table for User records."""

from passlib.apps import custom_app_context as pwd_context
from sqlalchemy import (
    Column,
    Integer,
    Unicode,
)
from sqlalchemy.orm import relationship

from .meta import Base


class User(Base):
    """Create a table for users."""

    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    books = relationship("Book", back_populates="user")

    first_name = Column(Unicode)
    last_name = Column(Unicode)
    email = Column(Unicode, nullable=False, unique=True)
    password = Column(Unicode, nullable=False)

    def __init__(self, *args, **kwargs):
        """Create a new User and store only the hashed password."""
        if 'password' in kwargs:
            kwargs['password'] = pwd_context.hash(kwargs['password'])

        super(User, self).__init__(*args, **kwargs)

    def verify(self, password):
        """Verify that the given password is correct."""
        return pwd_context.verify(password, self.password)

    def to_json(self):
        """Take all model attributes and render them as JSON."""
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email
        }
