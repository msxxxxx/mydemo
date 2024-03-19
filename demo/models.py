from datetime import datetime, UTC

from src.models import Base

from sqlalchemy import (
    Column,
    CHAR,
    VARCHAR,
    CheckConstraint,
    TIMESTAMP,
    String,
    ForeignKey,
    INT
)
from sqlalchemy.orm import relationship

from src.models import Base

__all__ = [
    "Cases",
    "Comments",
    "User"
]


class Cases(Base):
    __table_args__ = (
        CheckConstraint(sqltext="length(title) >= 2"),
    )

    title = Column(
        VARCHAR(length=128),
        nullable=False,
    )
    slug = Column(
        VARCHAR(length=128),
        nullable=False,
        unique=True
    )
    date_created = Column(
        TIMESTAMP,
        default=lambda: datetime.now(tz=UTC),
        nullable=False
    )
    body = Column(String, nullable=False)
    case_comment = relationship(
        argument="Comments",
        back_populates="case_related"
    )


class Comments(Base):

    text = Column(
        VARCHAR(length=128),
        nullable=False,
    )
    date_created = Column(
        TIMESTAMP,
        default=lambda: datetime.now(tz=UTC),
        nullable=False
    )
    case_id = Column(
        INT,
        ForeignKey(
            column="demo_cases.id"
        ),
        # primary_key=True,
        index=True
    )
    case_related = relationship(
        argument="Cases",
        back_populates="case_comment"
    )

    def __str__(self) -> str:
        return self.text


class User(Base):
    email = Column(VARCHAR(length=128), nullable=False, unique=True)
    password = Column(CHAR(length=60), nullable=False)

    def __str__(self) -> str:
        return self.email