from datetime import datetime
from typing import Optional

from pydantic import BaseModel


# --- Request Schemas ---

class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    is_completed: Optional[bool] = None


# --- Response Schema ---

class TaskResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    is_completed: bool
    created_at: datetime
    updated_at: Optional[datetime]
    owner_id: int

    model_config = {"from_attributes": True}
