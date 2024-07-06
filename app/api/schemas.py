import uuid
from datetime import datetime
from typing import Generic, TypeVar, Optional, List

from pydantic import BaseModel

T = TypeVar("T")


class UserSchema(BaseModel):
    id: Optional[uuid.UUID] = None
    name: str = None
    surname: str = None
    login: Optional[str] = None
    password: Optional[str] = None
    role: Optional[str] = None
    created_at: datetime = None
    updated_at: Optional[datetime] = None


class FeedbacksSchema(BaseModel):
    id: Optional[uuid.UUID] = None
    feedback: str = None
    question_id: str = None
    created_at: datetime = None
    updated_at: Optional[datetime] = None


class VariantsSchema(BaseModel):
    id: Optional[uuid.UUID] = None
    name: str = None
    question_id: uuid.UUID = None
    created_at: datetime = None
    updated_at: Optional[None] = None

    class Config:
        orm_mode = True


class QuestionsSchema(BaseModel):
    id: uuid.UUID
    name: str
    type: str
    created_at: datetime
    updated_at: Optional[datetime]
    variants: List[VariantsSchema]

    class Config:
        orm_mode = True


class Response(BaseModel, Generic[T]):
    code: int
    status: str
    message: str
    total: Optional[int] = None
    result: Optional[T] = None
    info: Optional[dict] = None
    role: Optional[str] = None


class LoginSchema(BaseModel):
    login: str
    password: str
