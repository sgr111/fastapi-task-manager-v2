from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.task import Task
from app.schemas.task import TaskCreate, TaskUpdate


async def get_tasks_by_user(db: AsyncSession, user_id: int) -> List[Task]:
    result = await db.execute(select(Task).where(Task.owner_id == user_id))
    return result.scalars().all()


async def get_task_by_id(db: AsyncSession, task_id: int, user_id: int) -> Optional[Task]:
    result = await db.execute(
        select(Task).where(Task.id == task_id, Task.owner_id == user_id)
    )
    return result.scalar_one_or_none()


async def create_task(db: AsyncSession, task_data: TaskCreate, user_id: int) -> Task:
    task = Task(**task_data.model_dump(), owner_id=user_id)
    db.add(task)
    await db.commit()
    await db.refresh(task)
    return task


async def update_task(db: AsyncSession, task: Task, task_data: TaskUpdate) -> Task:
    update_fields = task_data.model_dump(exclude_unset=True)
    for field, value in update_fields.items():
        setattr(task, field, value)
    await db.commit()
    await db.refresh(task)
    return task


async def delete_task(db: AsyncSession, task: Task) -> None:
    await db.delete(task)
    await db.commit()
