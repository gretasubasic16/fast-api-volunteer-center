from pydantic import BaseModel
from typing import List
from datetime import datetime

class VolunteerBase(BaseModel):
    name: str
    email: str

class VolunteerCreate(VolunteerBase):
    pass

class VolunteerResponse(BaseModel):
    id: str
    name: str
    email: str


# Pydantic model for Coordinator
class CoordinatorBase(BaseModel):
    name: str
    email: str

class CoordinatorCreate(CoordinatorBase):
    pass

class CoordinatorResponse(BaseModel):
    id: str
    name: str
    email: str

# Pydantic model for VolunteerProject
class VolunteerProjectBase(BaseModel):
    name: str
    description: str
    start_date: datetime
    end_date: datetime
    coordinator: str

class VolunteerProjectCreate(VolunteerProjectBase):
    pass

class VolunteerProjectResponse(BaseModel):
    id: str
    name: str
    description: str
    start_date: datetime
    end_date: datetime
    coordinator: str  # Use CoordinatorResponse for coordinator field


# Pydantic model for ProjectReservation
class ProjectReservationBase(BaseModel):
    project_id: str
    volunteer_id: str

class ProjectReservationCreate(ProjectReservationBase):
    pass

class ProjectReservationResponse(BaseModel):
    id: str
    project_id: str
    volunteer_id: str