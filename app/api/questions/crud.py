import datetime
import uuid
from typing import List

from sqlalchemy.orm import Session

from app.api.models import Questions, Variants
from app.api.schemas import QuestionsSchema, VariantsSchema


def get_question(db: Session):
    return db.query(Questions).all()


def get_variants(db: Session, question_id: uuid.UUID):
    return db.query(Variants).filter(Variants.question_id == question_id).all()


def get_question_by_id(db: Session, question_id: uuid.UUID):
    return db.query(Questions).filter(Questions.id == question_id).first()


def syn_question(
    db: Session,
    questions: List[QuestionsSchema],
):
    for question in questions:
        if not question.id:
            _question = Questions(
                name=question.name,
                type=question.type,
                created_at=datetime.datetime.now(),
            )
            db.add(_question)
            db.flush()
            if question.variants:
                for variant in question.variants:
                    if not variant.id:
                        _variant = Variants(
                            name=variant.name,
                            question_id=_question.id,
                            created_at=datetime.datetime.now(),
                        )
                        db.add(_variant)
                        db.commit()
                    else:
                        update_variant(db, variant, variant.question_id)
        else:
            update_question(db, question, question.id)
            db.commit()
        db.commit()


def delete_question(db: Session, question_id: uuid.UUID):
    db.query(Questions).filter(Questions.id == question_id).delete()
    db.commit()


def update_question(db: Session, question: QuestionsSchema, question_id: uuid.UUID):
    _question = get_question_by_id(db=db, question_id=question_id)
    _question.name = question.name
    _question.type = question.type
    if question.variants:
        for variant in question.variants:
            if not variant.id:
                _variant = Variants(
                    name=variant.name,
                    question_id=_question.id,
                    created_at=datetime.datetime.now(),
                )
                db.add(_variant)
                db.commit()
            else:
                update_variant(db, variant, variant.question_id)
    _question.updated_at = datetime.datetime.now()
    db.commit()
    db.refresh(_question)
    return _question

def update_variant(db: Session, variant: VariantsSchema, question_id: uuid.UUID):
    _variant = db.query(Variants).filter(Variants.question_id == question_id).first()
    _variant.name = variant.name
    _variant.updated_at = datetime.datetime.now()
    db.commit()
    db.refresh(_variant)
    return _variant
