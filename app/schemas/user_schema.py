from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    full_name: str = Field(..., min_length=2)
    email: EmailStr
    password: str = Field(..., min_length=10)


class UserResponse(BaseModel):
    id: int

    full_name: str

    email: EmailStr
    role: str
    is_active: bool




    class Config:
        from_attributes = True