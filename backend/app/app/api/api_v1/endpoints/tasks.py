from fastapi import APIRouter, HTTPException, Depends

from app.api.deps import get_current_user
from app.utils import Prefix, Tag
from app.celery_worker import celery_app
from app.models import User
from app.models.task import TaskRead

router = APIRouter(prefix=Prefix.tasks, tags=[Tag.tasks])


@router.get("/{id}", response_model=TaskRead)
def read_task(*, current_user: User = Depends(get_current_user), id: str):
    result = celery_app.AsyncResult(id)
    if result.result and not result.result.get("picture"):
        raise HTTPException(
            status_code=result.result.get("status_code"),
            detail=result.result.get("detail"),
        )
    return {
        "task_id": result.id,
        "task_status": result.status,
        "task_result": result.result,
    }
