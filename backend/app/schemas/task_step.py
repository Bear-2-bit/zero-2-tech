from pydantic import BaseModel, ConfigDict, Field, field_validator


class TaskStepsSave(BaseModel):
    steps: list[str] = Field(
        min_length=1,
        max_length=8,
    )

    @field_validator("steps")
    @classmethod
    def validate_steps(
        cls,
        values: list[str],
    ) -> list[str]:
        cleaned_steps = []

        for value in values:
            value = value.strip()

            if not value:
                raise ValueError(
                    "step cannot be empty"
                )

            cleaned_steps.append(value)

        return cleaned_steps


class TaskStepUpdate(BaseModel):
    content: str | None = Field(
        default=None,
        min_length=1,
        max_length=500,
    )

    is_done: bool | None = None

    @field_validator("content")
    @classmethod
    def validate_content(
        cls,
        value: str | None,
    ):
        if value is None:
            return value

        value = value.strip()

        if not value:
            raise ValueError(
                "content cannot be empty"
            )

        return value


class TaskStepResponse(BaseModel):
    id: int
    task_id: int
    content: str
    is_done: bool
    sort_order: int

    model_config = ConfigDict(
        from_attributes=True
    )