import uuid

from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from app.api.schemas import Response, VideoSchema
from app.api.questions.crud import (
    get_video,
    get_video_by_id,
    create_video,
    delete_video,
    update_video,
    count_videos,
)
from app.db import get_db
from app.utils.auth_middleware import get_current_user

router = APIRouter()


@router.get("/{video_id}")
async def get_video_by_id_route(
    video_id: uuid.UUID,
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    _video = get_video_by_id(db, video_id)
    return Response(
        code=200, status="ok", message="success", result=_video
    ).model_dump()


@router.get("/")
async def get_videos_route(
    req: Request,
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    limit = int(req.query_params.get("results") or 10)
    skip = int(req.query_params.get("page") or 1) - 1
    _videos = get_video(
        db,
        limit=limit,
        skip=skip,
        order_by=req.query_params.get("order"),
        search=req.query_params.get("search"),
    )
    _count_of_videos = count_videos(db)

    return Response(
        code=200,
        status="ok",
        message="success",
        result=[
            {
                "id": video.id,
                "name": video.name,
                "video_url": video.login,
                "created_at": video.created_at,
                "updated_at": video.updated_at,
            }
            for video in _videos
        ],
        total=_count_of_videos,
        info={"result": limit, "page": skip},
    ).dict()


@router.post("/")
async def create_video_route(
    video: VideoSchema,
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    create_video(db, video)
    return Response(code=201, status="ok", message="created").dict()


@router.delete("/{video_id}")
async def delete_video_route(
    video_id: uuid.UUID,
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    delete_video(db, video_id)
    return Response(
        code=200,
        status="ok",
        message="deleted",
    ).model_dump()


@router.put("/{video_id}")
async def update_video_route(
    video_id: uuid.UUID,
    video: VideoSchema,
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    _video = update_video(db, video, video_id)
    return Response(
        code=200, status="ok", message="updated", result=_video
    ).model_dump()
