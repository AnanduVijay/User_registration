import base64
from fastapi import UploadFile

from sqlalchemy.orm import Session
from passlib.context import CryptContext

from pymongo.database import Database
from pymongo.collection import Collection

from users import schema
from users import models
from users.models import User
from users.exceptions import UserExistException, UserNotFoundException


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_user_by_email(email, db):
    user = db.query(models.User).filter(models.User.email == user.email).first()
    return user


def create_user(
    db: Session,
    mongo_db: Database,
    user: schema.UserCreate,
    profile_picture: UploadFile,
):
    """
    Creates a user in the database and if the user exists apprpriate error is raisesd
    """
    # get profile picture mongo table
    profile_picture_collection: Collection = mongo_db.profile_picture
    # encode profile picture to base64 encoded format to be saved in DB
    encoded_profile_pic = base64.b64encode(profile_picture.file.read()).decode("utf-8")
    existing_user = get_user_by_email(user.email, db)
    if existing_user:
        raise UserExistException()

    hashed_password = pwd_context.hash(user.password)

    new_user = models.User(
        full_name=user.full_name,
        email=user.email,
        password=hashed_password,
        phone=user.phone,
    )
    db.add(new_user)
    db.commit()

    profile_pic_data = schema.UserProfile(_id=new_user.id, profile_picture = encoded_profile_pic)
    profile_pic = profile_picture_collection.insert_one(
        profile_pic_data.model_dump(by_alias=True)
    )
    image = profile_picture_collection.find_one({"_id": new_user.id})
    return new_user, image


def get_user_by_id(user_id, db: Session, mongo_db: Database):
    profile_picture_collection: Collection = mongo_db.profile_picture

    user = db.query(models.User).filter(models.User.id == user_id).first()
    profile_picture = profile_picture_collection.find_one({"_id": user.id})

    if user is None:
        raise UserNotFoundException()

    return user, profile_picture
