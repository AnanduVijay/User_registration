from sqlalchemy import Column, Integer, String
from database.postgres import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    full_name = Column(String(50), nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String(100), nullable=False)
    phone = Column(String, nullable=False)
