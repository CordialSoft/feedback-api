import uuid
from io import BytesIO
from typing import List

from openpyxl import Workbook
from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from starlette.responses import StreamingResponse

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
alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'


@router.get("/download")
async def download_feedbacks(
        db: Session = Depends(get_db),
        _=Depends(get_current_user),
):
    wb = Workbook()
    ws = wb.active
    _feedback = get_feedback(db)
    questions = set([feedback.question for feedback in _feedback])

    all_feedbacks = [
            {
                "question": data,
                "feedback": [feedback.feedback for feedback in _feedback if feedback.question == data]
            }
            for data in questions]

    for index, feedback in enumerate(all_feedbacks):
        ws[f"{alphabet[index]}{1}"] = feedback['question']
        ws.column_dimensions[f"{alphabet[index]}"].width = 30
        for index2, feed in enumerate(feedback['feedback']):
            ws[f'{alphabet[index]}{index2+2}'] = feed

    buffer = BytesIO()
    wb.save(buffer)
    buffer.seek(0)

    return StreamingResponse(
        buffer,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": "attachment; filename=result.xlsx"},
    )


@router.get("/v2")
async def get_feedbacks_route(
        req: Request,
        db: Session = Depends(get_db),
        _=Depends(get_current_user),
):
    _feedbacks = get_feedback(db, search=req.query_params.get("search"))
    questions = set([feedback.question for feedback in _feedbacks])

    return Response(
        code=200,
        status="ok",
        message="success",
        result=[
            {
                "question": data,
                "feedback": [feedback.feedback for feedback in _feedbacks if feedback.question == data]
            }
            for data in questions],
        total=0,
    ).dict()


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
        db: Session = Depends(get_db),
        _=Depends(get_current_user),
):
    _feedbacks = get_feedback(db)

    return Response(
        code=200,
        status="ok",
        message="success",
        result=[
            {
                "id": feedback.id,
                "feedback": feedback.feedback,
                "question": feedback.question,
                "created_at": feedback.created_at,
                "updated_at": feedback.updated_at,
            }
            for feedback in _feedbacks
        ],
        total=0,
    ).dict()


@router.post("/")
async def create_feedback_route(
        feedback: List[FeedbacksSchema],
        db: Session = Depends(get_db)
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
