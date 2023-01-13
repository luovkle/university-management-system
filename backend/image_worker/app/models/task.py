from pydantic import BaseModel


class TaskIDRead(BaseModel):
    task_id: str


class TaskResultRead(BaseModel):
    picture: str


class TaskRead(TaskIDRead):
    task_status: str
    task_result: TaskResultRead | None = None
