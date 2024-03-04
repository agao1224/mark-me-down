from sqlalchemy import Column, Integer, String, ARRAY

from database import Base


class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True)
    title = Column(String, index=True)
    form_link = Column(String)
    subscribers = Column(String, default="")
