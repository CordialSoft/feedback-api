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


@router.get("/download")
async def download_feedbacks(
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    wb = Workbook()
    ws = wb.active

    _feedback = get_feedback(db)
    ws["A1"] = "Savol"
    ws["B1"] = "Feedback"
    ws["C1"] = "Vaqt"

    for index, item in enumerate(_feedback):
        ws[f"A{index + 2}"] = item.feedback
        ws[f"B{index + 2}"] = item.question
        ws[f"C{index + 2}"] = item.created_at

    ws.column_dimensions["A"].width = 30
    ws.column_dimensions["B"].width = 30
    ws.column_dimensions["C"].width = 30
    buffer = BytesIO()
    wb.save(buffer)
    buffer.seek(0)

    return StreamingResponse(
        buffer,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": "attachment; filename=result.xlsx"},
    )


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
