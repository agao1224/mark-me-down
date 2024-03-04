from sqlalchemy.orm import Session
import models
import schemas

import os 
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, To


def send_emails(recipients, form_link, course_title):
    for email in recipients:
        if len(email) == 0:
            continue

        try:
            message = Mail(
                from_email='agao2@andrew.cmu.edu',
                to_emails=email,
                subject=f"{course_title} Attendance Link",
                html_content=f"<p> Link here: {form_link} </p>",
            )
            
            sg = SendGridAPIClient(os.environ.get("SENDGRID_API_KEY"))
            response = sg.send(message)
            print(response.status_code)
            print(response.body)
            print(response.headers)
            print("Email sent successfully!")
        except Exception as e:
            print(e)


def create_course(db: Session, course: schemas.CourseCreate):
    existing_course = db.query(models.Course).filter(models.Course.title == course.title).first()

    if existing_course:
        print(f"{course.title} already exists!")
        return None

    course = models.Course(**course.model_dump())
    db.add(course)
    db.commit()
    db.refresh(course)
    return course


def get_courses(db: Session):
    return db.query(models.Course).all()


def add_email_to_course(db: Session, course_title: str, email: str):
    course = db.query(models.Course).filter(models.Course.title == course_title).first()
    if course:
        subscribers = str(course.subscribers.split(","))
        if email not in subscribers:
            course.subscribers = f"{course.subscribers}{email},"
            db.commit()
            db.refresh(course)
            return course
        print("Email already subscribed to course")
        return None
    
    print("Course not found")
    return None


def update_course_form_link(db: Session, course_title: str, form_link: str, ):
    course = db.query(models.Course).filter(models.Course.title == course_title).first()
    if course:
        # Update link
        course.form_link = form_link
        db.commit()
        db.refresh(course)

        # Broadcast to all subscribers
        subscribers = course.subscribers.split(",")
        send_emails(subscribers, form_link, course_title)
        return True

    print("Course not found")
    return False