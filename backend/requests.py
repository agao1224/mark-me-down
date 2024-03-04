from pydantic import BaseModel

class Subscription(BaseModel):
    title: str
    email: str

class LinkUpdate(BaseModel):
    form_link: str
    course_title: str