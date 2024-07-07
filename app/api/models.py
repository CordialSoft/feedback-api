import datetime
import uuid

from sqlalchemy import Column, UUID, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from app.db import Base, engine


class Users(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, index=True, nullable=False)
    surname = Column(String, index=True, nullable=False)
    company_logo = Column(String, nullable=True)
    company_name = Column(String, nullable=True)
    login = Column(String, nullable=True, unique=True)
    password = Column(String, nullable=True)
    role = Column(String, default="user")
    created_at = Column(DateTime, default=datetime.datetime.now)
    updated_at = Column(DateTime)


class Feedbacks(Base):
    __tablename__ = "feedbacks"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    feedback = Column(String, nullable=True)
    question_id = Column(UUID(as_uuid=True), ForeignKey("questions.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.now)
    updated_at = Column(DateTime)


class Questions(Base):
    __tablename__ = "questions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    type = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.now)
    updated_at = Column(DateTime)
    variants = relationship(
        "Variants", back_populates="question", cascade="all, delete-orphan"
    )


class Variants(Base):
    __tablename__ = "variants"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    question_id = Column(UUID(as_uuid=True), ForeignKey("questions.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.now)
    updated_at = Column(DateTime)
    question = relationship("Questions", back_populates="variants")


Base.metadata.create_all(bind=engine)
