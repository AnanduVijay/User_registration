from fastapi import (
    APIRouter,
    Depends,
    Form,
    HTTPException,
    UploadFile,
    File,
    status,
)
from fastapi.encoders import jsonable_encoder
from pydantic import ValidationError

from sqlalchemy.orm import Session
from pymongo.database import Database
from database.mongo.connections import get_mongodb
from database.postgres.connections import get_db
from users import schema
from users.crud import create_user, get_user_by_id
from users.exceptions import UserExistException, UserNotFoundException

router = APIRouter(prefix="/users")


def checker(data: str = Form(...)):
    try:
        return schema.UserCreate.model_validate_json(data)
    except ValidationError as e:
        raise HTTPException(
            detail=jsonable_encoder(e.errors()),
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )


@router.post("/register", response_model=schema.User)
def register_user(
    user: schema.UserCreate = Depends(checker),
    db: Session = Depends(get_db),
    mongo_db: Database = Depends(get_mongodb),
    profile_picture: UploadFile = File(...),
):
    """
    Creates a user with the provided data
    """
    try:
        user = create_user(db, mongo_db, user, profile_picture)
        return user
    except UserExistException:
        raise HTTPException(status_code=400, detail="User already exists")


@router.get("/user/{user_id}", response_model=schema.User)
def user_details(
    user_id: int,
    db: Session = Depends(get_db),
    mongo_db: Database = Depends(get_mongodb),
):
    """
    Return's information abou a registered user with the provided primary key
    """
    try:
        user = get_user_by_id(user_id, db, mongo_db)
        return user
    except UserNotFoundException:
        raise HTTPException(status_code=404, detail="User not found")


