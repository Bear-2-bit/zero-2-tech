from fastapi import APIRouter, Depends
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.database import get_db
from app.models.task import Task
from app.models.user import User
from app.schemas.dashboard import DashboardResponse


router = APIRouter(
    prefix="/api/dashboard",
    tags=["dashboard"],
)


@router.get(
    "",
    response_model=DashboardResponse,
)
def get_dashboard(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    total_statement = (
        select(func.count(Task.id))
        .where(
            Task.user_id == current_user.id
        )
    )

    completed_statement = (
        select(func.count(Task.id))
        .where(
            Task.user_id == current_user.id,
            Task.status == "done",
        )
    )

    total_tasks = db.scalar(total_statement) or 0

    completed_tasks = (
        db.scalar(completed_statement) or 0
    )

    completion_rate = (
        completed_tasks / total_tasks * 100
        if total_tasks > 0
        else 0
    )

    return {
        "total_tasks": total_tasks,
        "completed_tasks": completed_tasks,
        "completion_rate": round(
            completion_rate,
            1,
        ),
    }