from pydantic import BaseModel, Field


class AIDecomposeRequest(BaseModel):
    goal: str = Field(
        min_length=2,
        max_length=200,
    )


class AIDecomposeResponse(BaseModel):
    steps: list[str]