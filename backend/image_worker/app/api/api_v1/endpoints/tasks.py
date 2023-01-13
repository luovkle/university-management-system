from fastapi import APIRouter, HTTPException

from app.utils import Tag, Prefix
from app.core.celery import celery_app
from app.models.task import TaskRead

router = APIRouter(prefix=Prefix.tasks, tags=[Tag.tasks])


@router.get("/{id}", response_model=TaskRead)
def read_task(id: str):
    result = celery_app.AsyncResult(id)
    data = result.result
    if not data:
        raise HTTPException(
            status_code=404,
            detail="Task not found",
        )
    if data.get("status_code"):
        raise HTTPException(
            status_code=data["status_code"],
            detail=data["detail"],
        )
    return {
        "task_id": result.id,
        "task_status": result.status,
        "task_result": result.result,
    }
