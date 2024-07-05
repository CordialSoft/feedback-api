import uuid

from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from app.api.feedbacks.crud import (
    get_feedback,
    get_feedback_by_id,
    create_feedback,
    delete_feedback,
)
from app.api.schemas import Response, FeedbacksSchema
from app.db import get_db
from app.utils.auth_middleware import get_current_user

router = APIRouter()


@router.get("/{feedback_id}")
async def get_feedback_by_id_route(
    feedback_id: uuid.UUID,
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    _feedback = get_feedback_by_id(db, feedback_id)
    return Response(
        code=200, status="ok", message="success", result=_feedback
    ).model_dump()


@router.get("/")
async def get_feedbacks_route(
    req: Request,
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    limit = int(req.query_params.get("results") or 10)
    skip = int(req.query_params.get("page") or 1) - 1
    _feedbacks = get_feedback(
        db,
        limit=limit,
        skip=skip,
    )

    return Response(
        code=200,
        status="ok",
        message="success",
        result=[
            {
                "id": feedback.id,
                "name": feedback.name,
                "feedback_url": feedback.feedback_url,
                "created_at": feedback.created_at,
                "updated_at": feedback.updated_at,
            }
            for feedback in _feedbacks
        ],
        total=10,
        info={"result": limit, "page": skip},
    ).dict()


@router.post("/")
async def create_feedback_route(
    feedback: FeedbacksSchema,
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    create_feedback(db, feedback)
    return Response(code=201, status="ok", message="created").dict()


@router.delete("/{feedback_id}")
async def delete_feedback_route(
    feedback_id: uuid.UUID,
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    delete_feedback(db, feedback_id)
    return Response(
        code=200,
        status="ok",
        message="deleted",
    ).model_dump()
