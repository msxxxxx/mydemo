from datetime import datetime
from datetime import datetime, UTC

from sqlalchemy import (
    Column,
    VARCHAR,
    CheckConstraint,
    TIMESTAMP,
    String,
    BOOLEAN,
    BIGINT,
    ForeignKey,
    inspect, INT, create_engine,
)
from sqlalchemy.orm import relationship

from src.models import Base

__all__ = [
    "Cases",
    "Comments",
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

    def __str__(self) -> str:
        return self.title

class Comments(Base):
    # __table_args__ = (
    #     CheckConstraint(sqltext="length(title) >= 2"),
    # )

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
        primary_key=True,
        index=True
    )
    case_related = relationship(
        argument="Cases",
        back_populates="case_comment"
    )

    # def __str__(self) -> str:
    #     return self.text

