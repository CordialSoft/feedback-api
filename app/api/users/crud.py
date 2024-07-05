import datetime
import hashlib
import uuid
from typing import Optional

from sqlalchemy import func, or_
from sqlalchemy.orm import Session

from app.api.models import Users
from app.api.schemas import UserSchema


def get_user(
    db: Session,
    skip: int = 0,
    limit: int = 10,
    order_by: Optional[str] = None,
    search: Optional[str] = None,
):
    if skip < 0:
        skip = 0

    query = db.query(Users)
    if search:
        search = f"%{search}%"
        query = query.filter(or_(Users.name.ilike(search), Users.surname.ilike(search)))

    if order_by == "descend":
        query = query.order_by(Users.name.desc())
    elif order_by == "ascend":
        query = query.order_by(Users.name.asc())
    else:
        query = query.order_by(Users.created_at.desc())

    return query.offset(skip * limit).limit(limit).all()


def count_users(db: Session):
    return db.query(func.count(Users.id)).scalar()


def get_user_by_id(db: Session, user_id: uuid.UUID):
    return db.query(Users).filter(Users.id == user_id).first()


def create_user(db: Session, user: UserSchema):
    _user = Users(
        name=user.name,
        surname=user.surname,
        login=user.login,
        password=hashlib.sha256(user.password.encode()).hexdigest(),
        created_at=datetime.datetime.now(),
        role=user.role,
    )
    db.add(_user)
    db.commit()
    db.refresh(_user)
    return _user


def delete_user(db: Session, user_id: uuid.UUID):
    db.query(Users).filter(Users.id == user_id).delete()
    db.commit()


def update_user(db: Session, user: UserSchema, user_id: uuid.UUID):
    _user = get_user_by_id(db=db, user_id=user_id)
    _user.name = user.name
    _user.surname = user.surname
    _user.login = user.login
    _user.password = (hashlib.sha256(user.password.encode()).hexdigest(),)
    _user.updated_at = (datetime.datetime.now(),)
    _user.role = user.role
    db.commit()
    db.refresh(_user)
    return _user
