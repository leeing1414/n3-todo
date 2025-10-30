from pydantic import AliasChoices, BaseModel, ConfigDict, Field


class LoginRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    identifier: str = Field(
        ...,
        description="User login identifier (email or username)",
        min_length=1,
        validation_alias=AliasChoices("email", "username"),
    )
    password: str = Field(..., description="User password", min_length=8)


class RegisterRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    identifier: str = Field(
        ...,
        description="Desired login identifier (email or username)",
        min_length=1,
        validation_alias=AliasChoices("email", "username"),
    )
    name: str = Field(..., description="Display name for the user", min_length=1)
    password: str = Field(..., description="Account password", min_length=8)
    department: str | None = Field(
        default=None,
        description="Optional department label for the user",
    )
