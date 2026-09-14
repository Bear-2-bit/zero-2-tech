from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Path,
    status,
)
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.task import Task
from app.schemas.task import (
    TaskCreate,
    TaskResponse,
    TaskUpdate,
)
from app.core.dependencies import get_current_user
from app.models.user import User

router = APIRouter(
    prefix="/api/tasks",
    tags=["tasks"],
)


def get_task_or_404(
    task_id: int,
    user_id: int,
    db: Session,
) -> Task:
    statement = select(Task).where(
        Task.id == task_id,
        Task.user_id == user_id,
    )

    task = db.scalar(statement)

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    return task


@router.post(
    "",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_task(
    task_data: TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    ),
):
    task = Task(
        user_id=current_user.id,
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
    current_user: User = Depends(
        get_current_user
    ),
):
    statement = (
        select(Task)
        .where(
            Task.user_id == current_user.id
        )
        .order_by(Task.id.desc())
    )

    tasks = db.scalars(statement).all()

    return tasks


@router.get(
    "/{task_id}",
    response_model=TaskResponse,
)
def get_task(
    task_id: int = Path(gt=0),
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    ),
):
    return get_task_or_404(
        task_id=task_id,
        user_id=current_user.id,
        db=db,
    )

@router.put(
    "/{task_id}",
    response_model=TaskResponse,
)
def update_task(
    task_data: TaskUpdate,
    task_id: int = Path(gt=0),
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    ),
):
    task = get_task_or_404(
        task_id=task_id,
        user_id=current_user.id,
        db=db,
    )

    update_data = task_data.model_dump(
        exclude_unset=True
    )

    for field, value in update_data.items():
        setattr(task, field, value)

    db.commit()
    db.refresh(task)

    return task


@router.delete(
    "/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_task(
    task_id: int = Path(gt=0),
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    ),
):
    task = get_task_or_404(
        task_id=task_id,
        user_id=current_user.id,
        db=db,
    )

    db.delete(task)
    db.commit()