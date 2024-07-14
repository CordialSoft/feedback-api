import datetime
import uuid
from typing import List, Optional

from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.api.models import Feedbacks
from app.api.questions.crud import get_question_by_id
from app.api.schemas import FeedbacksSchema


def get_feedback(db: Session, search: Optional[str] = None):
    query = db.query(Feedbacks)
    if search != "undefined" != 'null':
        search = f"%{search}%"
        query = query.filter(
            or_(Feedbacks.feedback.ilike(search))
        )
    return (
        query.order_by(Feedbacks.created_at.desc())
        .all()
    )


def get_feedback_by_id(db: Session, feedback_id: uuid.UUID):
    return db.query(Feedbacks).filter(Feedbacks.id == feedback_id).first()


def create_feedback(db: Session, feedbacks: List[FeedbacksSchema]):
    for feedback in feedbacks:
        _feedback = Feedbacks(
            feedback=feedback.feedback,
            question=get_question_by_id(db, uuid.UUID(feedback.question)).name,
            created_at=datetime.datetime.now(),
        )
        db.add(_feedback)
        db.commit()
    db.commit()


def delete_feedback(db: Session, feedback_id: uuid.UUID):
    db.query(Feedbacks).filter(Feedbacks.id == feedback_id).delete()
    db.commit()
