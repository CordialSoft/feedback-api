import uuid
from typing import List

from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.orm import Session

from app.api.schemas import Response, QuestionsSchema, VariantsSchema
from app.api.questions.crud import (
    get_question,
    get_question_by_id,
    create_question,
    delete_question,
    update_question,
    get_variants,
)
from app.db import get_db
from app.utils.auth_middleware import get_current_user

router = APIRouter()


@router.get("/{question_id}")
async def get_question_by_id_route(
    question_id: uuid.UUID,
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    _question = get_question_by_id(db, question_id)
    if _question is None:
        raise HTTPException(status_code=404, detail="Question not found")
    return Response(
        code=200, status="ok", message="success", result=_question
    ).model_dump()


@router.get("/")
async def get_questions_route(
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    _questions = get_question(db)
    return Response(
        code=200,
        status="ok",
        message="success",
        result=[
            {
                "id": question.id,
                "name": question.name,
                "variants": get_variants(db, question.id),
                "type": question.type,
            }
            for question in _questions
        ],
        total=10,
    ).dict()


@router.post("/")
async def create_question_route(
    question: List[QuestionsSchema],
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    create_question(db, question)
    return Response(code=201, status="ok", message="created").dict()


@router.delete("/{question_id}")
async def delete_question_route(
    question_id: uuid.UUID,
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    delete_question(db, question_id)
    return Response(
        code=200,
        status="ok",
        message="deleted",
    ).model_dump()


@router.put("/{question_id}")
async def update_question_route(
    question_id: uuid.UUID,
    question: QuestionsSchema,
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    _question = update_question(db, question, question_id)
    return Response(
        code=200, status="ok", message="updated", result=_question
    ).model_dump()
