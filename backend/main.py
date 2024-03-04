from fastapi import Depends, FastAPI, HTTPException
from requests import (
    Subscription,
    LinkUpdate,
)

import crud
import models
import schemas
from sqlalchemy.orm import Session
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/courses/")
def create_course(
    course: schemas.CourseCreate, db : Session = Depends(get_db),
):
    course = crud.create_course(db=db, course=course)
    if course is None:
        raise HTTPException(status_code=400, detail="Course already exists.")
    return course


@app.get("/courses/")
def get_courses(
    db : Session = Depends(get_db),
):
    return crud.get_courses(db)


@app.put("/courses/")
def update_course(
    sub : Subscription, db : Session = Depends(get_db),
):
    course = crud.add_email_to_course(db=db,
                                       course_title=sub.title,
                                       email=sub.email)
    if not course:
        raise HTTPException(status_code=400, detail="Already subscribed or course doesn't exist")
    return course

@app.put("/courses/update_link")
def update_link(
    linkUpdate : LinkUpdate, db : Session = Depends(get_db),
):
    success = crud.update_course_form_link(db=db,
                                           course_title=linkUpdate.course_title,
                                           form_link=linkUpdate.form_link)
    if not success:
        raise HTTPException(status_code=400, detail="Failed to update link")
