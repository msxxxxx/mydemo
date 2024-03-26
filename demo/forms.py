from pydantic import Field, BaseModel


class CaseForm(BaseModel):
    title: str = Field(
        render_kw={"placeholder": "Your email"},
        default=...,
        min_length=2,
        max_length=128,
        title="Case Title",
        examples=["Кто убил мертвое море?"],
    )
    slug: str = Field(
        default=...,
        min_length=2,
        max_length=128,
        title="Case Title",
        examples=["kto-ubil-mertvoe-more"],
    )
    body: str = Field(default=..., min_length=1, title="Case Body", examples=["Me"])
