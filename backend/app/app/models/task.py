from sqlmodel import SQLModel


class TaskIDRead(SQLModel):
    task_id: str


class TaskResultRead(SQLModel):
    picture: str


class TaskRead(TaskIDRead):
    task_status: str
    task_result: TaskResultRead | None = None
