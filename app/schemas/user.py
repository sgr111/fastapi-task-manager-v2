from pydantic import BaseModel, EmailStr


# --- Request Schemas (what client sends) ---

class UserCreate(BaseModel):
    email: EmailStr
    username: str
    password: str


class UserLogin(BaseModel):
    username: str
    password: str


# --- Response Schemas (what API returns) ---

class UserResponse(BaseModel):
    id: int
    email: str
    username: str
    is_active: bool

    model_config = {"from_attributes": True}


# --- Token Schema ---

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
