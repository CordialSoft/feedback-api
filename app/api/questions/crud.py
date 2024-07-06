import datetime
import uuid
from typing import Optional, List

from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.api.models import Questions, Variants
from app.api.schemas import QuestionsSchema, VariantsSchema


def get_question(
    db: Session,
    skip: int = 0,
    limit: int = 10,
    search: Optional[str] = None,
):
    if skip < 0:
        skip = 0

    query = db.query(Questions)
    if search:
        search = f"%{search}%"
        query = query.filter(or_(Questions.name.ilike(search)))

    return query.offset(skip * limit).limit(limit).all()


def get_question_by_id(db: Session, question_id: uuid.UUID):
    return db.query(Questions).filter(Questions.id == question_id).first()


def create_question(
    db: Session,
    question: QuestionsSchema,
    variants: Optional[List[VariantsSchema]] = None,
):
    _question = Questions(
        name=question.name,
        type=question.type,
        created_at=datetime.datetime.now(),
    )
    db.add(_question)
    db.flush()
    if variants:
        for variant in variants:
            _variant = Variants(
                name=variant.name,
                question_id=_question.id,
                created_at=datetime.datetime.now(),
            )
            db.add(_variant)
            db.flush()
    db.commit()
    return _question


def delete_question(db: Session, question_id: uuid.UUID):
    db.query(Questions).filter(Questions.id == question_id).delete()
    db.commit()


def update_question(db: Session, question: QuestionsSchema, question_id: uuid.UUID):
    _question = get_question_by_id(db=db, question_id=question_id)
    _question.name = question.name
    _question.type = question.type
    _question.updated_at = datetime.datetime.now()
    db.commit()
    db.refresh(_question)
    return _question
