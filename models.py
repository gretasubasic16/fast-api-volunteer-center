from mongoengine import Document, StringField, EmailField, DateTimeField, ReferenceField
from pydantic import BaseModel

class UserLogin(BaseModel):
    email: str
    password: str

class Volunteer(Document):
    name = StringField(required=True)
    email = EmailField(unique=True, required=True)


class Coordinator(Document):
    name = StringField(required=True)
    email = EmailField(unique=True, required=True)

class VolunteerProject(Document):
    name = StringField(required=True)
    description = StringField()
    start_date = DateTimeField()
    end_date = DateTimeField()
    coordinator = ReferenceField(Coordinator)

class ProjectReservation(Document):
    project = ReferenceField(VolunteerProject)
    volunteer = ReferenceField(Volunteer)