"""Table for Book records."""

from sqlalchemy import (
    Column,
    Date,
    ForeignKey,
    Integer,
    Unicode,
)
from sqlalchemy.orm import relationship

from .meta import Base


class Book(Base):
    """Create a table for books."""

    __tablename__ = 'books'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    user = relationship("User", back_populates="books")

    title = Column(Unicode, nullable=False)
    author = Column(Unicode)
    isbn = Column(Unicode)
    pub_date = Column(Date)

    def to_json(self):
        """Take all model attributes and render them as JSON."""
        return {
            'id': self.id,
            'title': self.title,
            'author': self.author,
            'isbn': self.isbn,
            'pub_date': self.pub_date.strftime('%m/%d/%Y'),
        }
