from sqlalchemy import Column, String, DateTime
from app.database import Base
import uuid

class User(Base):
    __tablename__ = "users"

    external_id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    name = Column(String)
    email = Column(String, unique=True, index=True)
    date_of_birth = Column(DateTime)
