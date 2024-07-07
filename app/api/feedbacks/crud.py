import datetime
import uuid
from typing import List

from sqlalchemy.orm import Session

from app.api.models import Feedbacks, Questions
from app.api.schemas import FeedbacksSchema


def get_feedback(db: Session):
    query = db.query(Feedbacks, Questions)

    return (
        query.join(Feedbacks, Feedbacks.question_id == Questions.id)
        .order_by(Feedbacks.created_at.desc())
        .all()
    )


def get_feedback_by_id(db: Session, feedback_id: uuid.UUID):
    return db.query(Feedbacks).filter(Feedbacks.id == feedback_id).first()


def create_feedback(db: Session, feedbacks: List[FeedbacksSchema]):
    for feedback in feedbacks:
        _feedback = Feedbacks(
            feedback=feedback.feedback,
            question_id=uuid.UUID(feedback.question_id),
            created_at=datetime.datetime.now(),
        )
        db.add(_feedback)
        db.commit()
    db.commit()


def delete_feedback(db: Session, feedback_id: uuid.UUID):
    db.query(Feedbacks).filter(Feedbacks.id == feedback_id).delete()
    db.commit()
