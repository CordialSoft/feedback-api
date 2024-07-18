import os
import uuid

from fastapi import APIRouter, Depends, Request, File, UploadFile, HTTPException
from sqlalchemy.orm import Session
from starlette.responses import FileResponse

from app.api.schemas import Response, UserSchema, CompanySchema, LoginSchema
from app.api.users.crud import (
    get_user,
    get_user_by_id,
    create_user,
    delete_user,
    update_user,
    update_login_user,
)
from app.db import get_db
from app.utils.auth_middleware import get_current_user

router = APIRouter()
UPLOAD_FOLDER = "uploaded_folder"

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


@router.get("/files/{filename}")
async def get_file(filename: str):
    file_location = os.path.join(UPLOAD_FOLDER, filename)
    if os.path.exists(file_location):
        return FileResponse(file_location)
    return Response(
        code=404,
        status="not found",
        result={"message": "File not found"},
        message="ok",
    )


@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    file_extension = os.path.splitext(file.filename)[1]
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    file_location = os.path.join(UPLOAD_FOLDER, unique_filename)

    with open(file_location, "wb") as file_object:
        file_object.write(await file.read())

    return Response(
        code=201,
        status="ok",
        message="success",
        result={"file_id": unique_filename},
    )


@router.get("/get-me")
async def get_user_by_id_route(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    user_id = uuid.UUID(current_user["id"])
    _user = get_user_by_id(db, user_id)
    return Response(code=200, status="ok", message="success", result=_user).model_dump()


@router.get("/company")
async def get_user_by_id_route(
    db: Session = Depends(get_db),
):
    _user = get_user(db)
    return Response(code=200, status="ok", message="success", result=_user).model_dump()


@router.get("/{user_id}")
async def get_user_by_id_route(
    user_id: uuid.UUID,
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    _user = get_user_by_id(db, user_id)
    return Response(code=200, status="ok", message="success", result=_user).model_dump()


@router.get("/")
async def get_users_route(
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    _users = get_user(db)
    return Response(
        code=200,
        status="ok",
        message="success",
        result=[
            {
                "id": user.id,
                "name": user.name,
                "surname": user.surname,
                "login": user.login,
                "role": user.role,
                "created_at": user.created_at,
                "updated_at": user.updated_at,
            }
            for user in _users
        ],
        total=10,
    ).dict()


@router.post("/")
async def create_user_route(
    user: UserSchema,
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    create_user(db, user)
    return Response(code=201, status="ok", message="created").model_dump()


@router.delete("/{user_id}")
async def delete_user_route(
    user_id: uuid.UUID,
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    delete_user(db, user_id)
    return Response(
        code=200,
        status="ok",
        message="deleted",
    ).model_dump()


@router.put("/update_company")
async def update_user_route(
    company: CompanySchema,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    _user = update_user(db, company, current_user["id"])
    if _user == "not found":
        raise HTTPException(status_code=404, detail="User not found")
    return Response(
        code=200, status="ok", message="updated1", result=_user
    ).model_dump()


# @router.put("/{user_id}")
# async def update_user_route(
#     user_id: uuid.UUID,
#     user: UserSchema,
#     db: Session = Depends(get_db),
#     _=Depends(get_current_user),
# ):
#     _user = update_user(db, user, user_id)
#     return Response(code=200, status="ok", message="updated", result=_user).model_dump()


@router.put("/update")
async def update_user_route(
    user: LoginSchema,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    _user = update_login_user(db, user, current_user["id"])
    if _user == "not found":
        raise HTTPException(status_code=404, detail="Not found")
    return Response(code=200, status="ok", message="updated", result=_user).model_dump()
