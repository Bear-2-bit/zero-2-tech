from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.task import Task
from app.schemas.task import TaskCreate, TaskResponse


router = APIRouter(
    prefix="/api/tasks",
    tags=["tasks"],
)


@router.post(
    "",
    response_model=TaskResponse,
    status_code=201,
)
def create_task(
    task_data: TaskCreate,
    db: Session = Depends(get_db),
):
    task = Task(
        title=task_data.title,
        description=task_data.description,
    )

    db.add(task)

    db.commit()

    db.refresh(task)

    return task


@router.get(
    "",
    response_model=list[TaskResponse],
)
def get_tasks(
    db: Session = Depends(get_db),
):
    statement = select(Task)

    tasks = db.scalars(statement).all()

    return tasks