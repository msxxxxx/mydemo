from datetime import datetime, UTC
from typing import Optional

from pydantic import BaseModel, PositiveInt, EmailStr, Field, model_validator, ConfigDict, Json, ValidationError
from demo.types import PasswordStr

__all__ = [
    "CaseCreateForm",
    "CaseDetail",
    "CommentCreateForm",
    "CommentDetail",
    "UserLoginForm",
    "UserRegisterForm",
    "TokenPairDetail",
    "Schema"
]


class Schema(BaseModel):
    model_config = ConfigDict(
        use_enum_values=True,
        str_strip_whitespace=True,
        ser_json_bytes="utf8",
        ser_json_timedelta="float",
        allow_inf_nan=False
    )


class TokenPairDetail(Schema):
    user_name: str
    access_token: str
    refresh_token: str
    token_type: str


class CommentDetail(BaseModel):
    id: PositiveInt = Field(default=..., title="Comments ID", examples=[42])
    date_created: datetime = Field(default=..., title="Date of created comment")
    text: str = Field(
        default=...,
        min_length=2,
        max_length=128,
        text="Add comment",
        examples=["My first comment"],
    )
    case_id: PositiveInt = Field(default=..., title="Case ID", examples=[42])


class CaseCreateForm(BaseModel):
    title: str = Field(
        default=...,
        min_length=2,
        max_length=128,
        title="Case Title",
        examples=["My Case"],
    )
    body: str = Field(default=..., min_length=1, title="Case Body", examples=["Something happened"])
    # priority: str = Field(default=..., min_length=1, title="Case Body", examples=["pr"])
    # label: str = Field(default=..., min_length=1, title="Case Body", examples=["k"])
    category: str = Field(default=..., min_length=1, title="Case Body", examples=["yu"])
    # reported: str = Field(default=..., min_length=1, title="Case Body", examples=["uy"])
    # measures: str = Field(default=..., min_length=1, title="Case Body", examples=["uy"])
    # investigate: str = Field(default=..., min_length=1, title="Case Body", examples=["uy"])
    # recommendations: str = Field(default=..., min_length=1, title="Case Body", examples=["uyu"])



class CommentCreateForm(BaseModel):
    text: str = Field(
        default=...,
        min_length=2,
        max_length=128,
        text="Add comment",
        examples=["My first comment"],
    )


class CaseDetail(BaseModel):
    id: PositiveInt = Field(default=..., title="Case ID", examples=[42])
    date_created: datetime = Field(default=..., title="Date of created case")
    title: str = Field(
        default=...,
        min_length=2,
        max_length=128,
        title="Case Title",
        examples=["My Case"],
    )
    body: str = Field(default=..., min_length=1, title="Case Body", examples=["Something happened"])
    category: str = Field(default=..., min_length=1, title="C", examples=["Something"])
    comments: Optional[list[CommentDetail]] = Field(
        default=None, title="Cases Comments Details"
    )


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


