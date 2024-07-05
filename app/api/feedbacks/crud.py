import datetime
import uuid
from typing import Optional

from sqlalchemy import func, or_
from sqlalchemy.orm import Session

from app.api.models import Feedbacks
from app.api.schemas import FeedbacksSchema


def get_feedback(
    db: Session,
    skip: int = 0,
    limit: int = 10,
):
    if skip < 0:
        skip = 0

    query = db.query(Feedbacks)

    return (
        query.order_by(Feedbacks.created_at.desc())
        .offset(skip * limit)
        .limit(limit)
        .all()
    )


def get_feedback_by_id(db: Session, feedback_id: uuid.UUID):
    return db.query(Feedbacks).filter(Feedbacks.id == feedback_id).first()


def create_feedback(db: Session, feedback: FeedbacksSchema):
    _feedback = Feedbacks(
        feedback=feedback.feedback,
        question_id=feedback.question_id,
        created_at=datetime.datetime.now(),
    )
    db.add(_feedback)
    db.commit()
    db.refresh(_feedback)
    return _feedback


def delete_feedback(db: Session, feedback_id: uuid.UUID):
    db.query(Feedbacks).filter(Feedbacks.id == feedback_id).delete()
    db.commit()
