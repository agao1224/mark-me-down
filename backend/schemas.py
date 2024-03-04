from typing import List, Union

from pydantic import BaseModel

class CourseBase(BaseModel):
    title: str

class CourseCreate(CourseBase):
    pass

class Course(CourseBase):
    id: int
    subscribers: Union[str, None] = None
    form_link: Union[str, None] = None

    class Config:
        orm_mode = True
