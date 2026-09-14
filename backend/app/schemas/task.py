from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator


TaskStatus = Literal["todo", "doing", "done"]


class TaskCreate(BaseModel):
    title: str = Field(
        min_length=1,
        max_length=100,
    )
    description: str | None = Field(
        default=None,
        max_length=1000,
    )

    @field_validator("title")
    @classmethod
    def validate_title(cls, value: str) -> str:
        value = value.strip()

        if not value:
            raise ValueError("title cannot be empty")

        return value


class TaskUpdate(BaseModel):
    title: str | None = Field(
        default=None,
        min_length=1,
        max_length=100,
    )

    description: str | None = Field(
        default=None,
        max_length=1000,
    )

    status: TaskStatus | None = None

    @field_validator("title", mode="before")
    @classmethod
    def validate_title(cls, value):
        if value is None:
            raise ValueError("title cannot be null")

        value = value.strip()

        if not value:
            raise ValueError("title cannot be empty")

        return value

    @field_validator("status", mode="before")
    @classmethod
    def validate_status(cls, value):
        if value is None:
            raise ValueError("status cannot be null")

        return value


class TaskResponse(BaseModel):
    id: int
    title: str
    description: str | None
    status: TaskStatus
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)