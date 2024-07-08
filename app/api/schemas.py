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
    company_logo: Optional[str] = None
    company_name: Optional[str] = None
    password: Optional[str] = None
    role: Optional[str] = None
    created_at: datetime = None
    updated_at: Optional[datetime] = None


class CompanySchema(BaseModel):
    company_logo: str = None
    company_name: str = None


class FeedbacksSchema(BaseModel):
    id: Optional[uuid.UUID] = None
    feedback: str = None
    question: str = None
    created_at: datetime = None
    updated_at: Optional[datetime] = None


class VariantsSchema(BaseModel):
    id: Optional[uuid.UUID] = None
    name: str = None
    question_id: uuid.UUID = None
    created_at: datetime = None
    updated_at: Optional[None] = None


class QuestionsSchema(BaseModel):
    id: Optional[uuid.UUID] = None
    name: str = None
    type: str = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    variants: Optional[List[VariantsSchema]] = None


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
