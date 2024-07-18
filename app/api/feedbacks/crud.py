import datetime
import uuid
from typing import List, Optional

from sqlalchemy import or_, and_
from sqlalchemy.orm import Session

from app.api.models import Feedbacks, Answers
from app.api.questions.crud import get_question_by_id
from app.api.schemas import FeedbacksSchema


def get_feedback(db: Session, search: Optional[str] = None):
    query = db.query(Feedbacks)
    if search != "undefined" and search:
        search = f"%{search}%"
        query = query.filter(or_(Feedbacks.keywords.ilike(search)))
    return query.order_by(Feedbacks.created_at.desc()).all()


def get_answers(db: Session, feedback_id: uuid.UUID, question_id: uuid.UUID):
    result = (
        db.query(Answers.feedback)
        .filter(
            and_(Answers.feedback_id == feedback_id, Answers.question_id == question_id)
        )
        .order_by(Answers.created_at.asc())
        .all()
    )

    feedback_list = [row.feedback for row in result]
    return feedback_list


def get_feedback_by_id(db: Session, feedback_id: uuid.UUID):
    return db.query(Feedbacks).filter(Feedbacks.id == feedback_id).first()


def create_feedback(db: Session, feedbacks: List[FeedbacksSchema]):
    keywords = " ".join([feedback.feedback for feedback in feedbacks])
    _feedback = Feedbacks(keywords=keywords)
    db.add(_feedback)
    db.commit()
    for feedback in feedbacks:
        _answers = Answers(
            question=get_question_by_id(db, uuid.UUID(feedback.question)).name,
            feedback=feedback.feedback,
            feedback_id=_feedback.id,
            question_id=feedback.question,
        )
        db.add(_answers)
    db.commit()


def delete_feedback(db: Session, feedback_id: uuid.UUID):
    db.query(Feedbacks).filter(Feedbacks.id == feedback_id).delete()
    db.commit()
