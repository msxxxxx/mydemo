from datetime import datetime, UTC
from typing import Optional

from pydantic import BaseModel, PositiveInt, EmailStr, Field, model_validator
from demo.types import PasswordStr

__all__ = [
    "CasesCreateForm",
    "CasesDetail",
    "CasesCreateCommentForm",
    "CommentsDetail",
    "UserLoginForm",
    "UserRegisterForm"
]


class CommentsDetail(BaseModel):
    id: PositiveInt = Field(
        default=...,
        title="Comments ID",
        examples=[42]
    )
    date_created: datetime = Field(
        default=...,
        title="Date of created comment"
    )
    text: str = Field(
        default=...,
        min_length=2,
        max_length=128,
        text="Add comment",
        examples=["My first comment"]
    )
    case_id: PositiveInt = Field(
        default=...,
        title="Case ID",
        examples=[42]
    )


class CasesCreateForm(BaseModel):
    title: str = Field(
        default=...,
        min_length=2,
        max_length=128,
        title="Case Title",
        examples=["Кто убил мертвое море?"]
    )
    slug: str = Field(
        default=...,
        min_length=2,
        max_length=128,
        title="Case Title",
        examples=["kto-ubil-mertvoe-more"]
    )
    body: str = Field(
        default=...,
        min_length=1,
        title="Case Body",
        examples=["Me"]
    )


class CasesCreateCommentForm(BaseModel):
    text: str = Field(
        default=...,
        min_length=2,
        max_length=128,
        text="Add comment",
        examples=["My first comment"]
    )


class CasesDetail(BaseModel):
    id: PositiveInt = Field(
        default=...,
        title="Case ID",
        examples=[42]
    )
    date_created: datetime = Field(
        default=...,
        title="Date of created case"
    )
    slug: str = Field(
        default=...,
        min_length=2,
        max_length=128,
        title="Case Title",
        examples=["kto-ubil-mertvoe-more"]
    )
    title: str = Field(
        default=...,
        min_length=2,
        max_length=128,
        title="Case Title",
        examples=["Кто убил мертвое море?"]
    )
    body: str = Field(
        default=...,
        min_length=1,
        title="Case Body",
        examples=["Me"]
    )
    case_comment: Optional[list[CommentsDetail]] = Field(
        default=...,
        title="Cases Comments Details"
    )
    # name: Optional[str] = None

class UserRegisterForm(BaseModel):
    email: EmailStr
    password: PasswordStr = Field(default=..., min_length=8, max_length=64)
    confirm_password: PasswordStr = Field(default=..., min_length=8, max_length=64)

    @model_validator(mode="after")
    def check_passwords(self):
        if self.password != self.confirm_password:
            raise ValueError("password does not match confirm password")

        if self.email.lower().split("@")[0] in self.password.lower():
            raise ValueError("password has not contain email")

        return self


class UserLoginForm(BaseModel):
    email: EmailStr
    password: PasswordStr = Field(default=..., min_length=8, max_length=64)