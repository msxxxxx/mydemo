from datetime import datetime, UTC
from functools import partial
from sqlalchemy import (
    Column,
    CHAR,
    VARCHAR,
    CheckConstraint,
    TIMESTAMP,
    String,
    ForeignKey,
    INT,
)
from sqlalchemy.orm import relationship

from src.models import Base

__all__ = ["Case", "Comment", "User"]

class User(Base):
    __table_args__ = (CheckConstraint("length(email) >= 5"),)
    email = Column(VARCHAR(length=128), nullable=False, unique=True)
    password = Column(CHAR(length=60), nullable=False)
    cases = relationship("Case", back_populates="author")
    comments = relationship("Comment", back_populates="author")

    def __str__(self) -> str:
        return self.email


class Case(Base):
    __table_args__ = (CheckConstraint(sqltext="length(title) >= 2"),)

    title = Column(
        VARCHAR(length=128),
        nullable=False,
    )
    date_created = Column(
        TIMESTAMP(timezone=True),
        # default=lambda: datetime.now(tz=UTC),
        default=partial(datetime.now, tz=UTC),
        nullable=False,
    )
    body = Column(String, nullable=False)
    category = Column(String, nullable=True)
    comments = relationship(argument="Comment", back_populates="case")
    author_id = Column(INT, ForeignKey(column=User.id), index=True)
    #author_email = Column(VARCHAR, ForeignKey(column=User.email), index=True)
    author = relationship(argument="User", back_populates="cases")


class Comment(Base):
    __table_args__ = (CheckConstraint(sqltext="length(text) >= 2"),)
    text = Column(
        VARCHAR(length=128),
        nullable=False,
    )
    date_created = Column(
        TIMESTAMP(timezone=True), default=lambda: datetime.now(tz=UTC), nullable=False
    )
    author_id = Column(INT, ForeignKey(column=User.id), index=True)
    #author_email = Column(VARCHAR, ForeignKey(column=User.email), index=True)
    case_id = Column(INT, ForeignKey(column=Case.id), index=True)
    author = relationship(argument="User", back_populates="comments")
    case = relationship(argument="Case", back_populates="comments")


    def __str__(self) -> str:
        return self.text




