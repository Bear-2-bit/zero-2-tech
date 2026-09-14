import logging

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)

from app.core.dependencies import get_current_user
from app.models.user import User
from app.schemas.ai import (
    AIDecomposeRequest,
    AIDecomposeResponse,
)
from app.services.ai_service import decompose_goal


logger = logging.getLogger(__name__)


router = APIRouter(
    prefix="/api/ai",
    tags=["ai"],
)


@router.post(
    "/decompose",
    response_model=AIDecomposeResponse,
)
def decompose_task(
    data: AIDecomposeRequest,
    current_user: User = Depends(
        get_current_user
    ),
):
    try:
        steps = decompose_goal(
            data.goal
        )

        return {
            "steps": steps
        }

    except Exception:
        logger.exception(
            "DeepSeek API call failed"
        )

        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="AI service unavailable",
        )