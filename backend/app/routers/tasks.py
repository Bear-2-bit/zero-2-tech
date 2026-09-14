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

from sqlalchemy import delete, select

from app.models.task_step import TaskStep
from app.schemas.task_step import (
    TaskStepResponse,
    TaskStepsSave,
    TaskStepUpdate,
)

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

@router.post(
    "/{task_id}/steps",
    response_model=list[TaskStepResponse],
)
def save_task_steps(
    data: TaskStepsSave,
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

    db.execute(
        delete(TaskStep).where(
            TaskStep.task_id == task.id
        )
    )

    for index, content in enumerate(
        data.steps,
        start=1,
    ):
        step = TaskStep(
            task_id=task.id,
            content=content,
            sort_order=index,
        )

        db.add(step)

    db.commit()

    statement = (
        select(TaskStep)
        .where(
            TaskStep.task_id == task.id
        )
        .order_by(
            TaskStep.sort_order
        )
    )

    return db.scalars(statement).all()

@router.get(
    "/{task_id}/steps",
    response_model=list[TaskStepResponse],
)
def get_task_steps(
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

    statement = (
        select(TaskStep)
        .where(
            TaskStep.task_id == task.id
        )
        .order_by(
            TaskStep.sort_order
        )
    )

    return db.scalars(statement).all()

def get_step_or_404(
    step_id: int,
    task_id: int,
    db: Session,
) -> TaskStep:
    statement = select(TaskStep).where(
        TaskStep.id == step_id,
        TaskStep.task_id == task_id,
    )

    step = db.scalar(statement)

    if step is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task step not found",
        )

    return step

@router.put(
    "/{task_id}/steps/{step_id}",
    response_model=TaskStepResponse,
)
def update_task_step(
    data: TaskStepUpdate,
    task_id: int = Path(gt=0),
    step_id: int = Path(gt=0),
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

    step = get_step_or_404(
        step_id=step_id,
        task_id=task.id,
        db=db,
    )

    update_data = data.model_dump(
        exclude_unset=True
    )

    for field, value in update_data.items():
        setattr(step, field, value)

    db.commit()
    db.refresh(step)

    return step

@router.delete(
    "/{task_id}/steps/{step_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_task_step(
    task_id: int = Path(gt=0),
    step_id: int = Path(gt=0),
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

    step = get_step_or_404(
        step_id=step_id,
        task_id=task.id,
        db=db,
    )

    db.delete(step)
    db.commit()