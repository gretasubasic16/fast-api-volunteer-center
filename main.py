from fastapi import FastAPI, HTTPException, Path, Body
from pymongo import MongoClient
from decouple import config
from mongoengine import connect, Document, StringField, EmailField, DateTimeField, ReferenceField, ObjectIdField, DEFAULT_CONNECTION_NAME, DoesNotExist
from passlib.context import CryptContext
from models import Volunteer,UserLogin, Coordinator, ProjectReservation, VolunteerProject  # Import MongoDB Document models
from bson import ObjectId  # Import ObjectId from bson
from datetime import timedelta



from schemas import (
    VolunteerCreate, VolunteerResponse,
    CoordinatorCreate, CoordinatorResponse,
    VolunteerProjectCreate, VolunteerProjectResponse,
    ProjectReservationCreate, ProjectReservationResponse,
)
app = FastAPI()

# MongoDB connection
mongo_uri = config("MONGO_URI")
database_name = config("DATABASE_NAME")
connect(db=database_name, alias=DEFAULT_CONNECTION_NAME, host=mongo_uri)


client = MongoClient(mongo_uri)
db = client[database_name]


SECRET_KEY = "your-secret-key"  # Replace with your secret key
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI with MongoDB!"}



@app.get("/check_db")
def check_db_connection():
    try:
        client.server_info()
        return {"message": "Connected to the MongoDB database"}
    except Exception as e:
        return {"message": f"Error connecting to the MongoDB database: {str(e)}"}



@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI with MongoDB!"}

@app.get("/check_db")
def check_db_connection():
    try:
        client.server_info()
        return {"message": "Connected to the MongoDB database"}
    except Exception as e:
        return {"message": f"Error connecting to the MongoDB database: {str(e)}"}

# Volunteer Endpoints


@app.post("/volunteers/", response_model=VolunteerCreate)
async def create_volunteer(volunteer_data: VolunteerCreate):
    # Create a new Volunteer document
    new_volunteer = Volunteer(**volunteer_data.dict())

    # Save the Volunteer document to the database
    new_volunteer.save()

    # Return the created Volunteer object
    return new_volunteer

@app.get("/volunteers/{volunteer_id}", response_model=VolunteerCreate)
async def read_volunteer(volunteer_id: str = Path(..., description="Volunteer ID")):
    try:
        volunteer = Volunteer.objects.get(id=volunteer_id)
        return volunteer
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="Volunteer not found")

@app.put("/volunteers/{volunteer_id}", response_model=VolunteerResponse)
async def update_volunteer(
    volunteer_id: str,
    updated_volunteer: VolunteerCreate = Body(...)
):
    try:
        volunteer = Volunteer.objects.get(id=volunteer_id)
        volunteer.update(**updated_volunteer.dict())
        return volunteer
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="Volunteer not found")

@app.delete("/volunteers/{volunteer_id}", response_model=dict)
async def delete_volunteer(volunteer_id: str = Path(..., description="Volunteer ID")):
    try:
        volunteer = Volunteer.objects.get(id=volunteer_id)
        volunteer.delete()
        return {"message": "Volunteer deleted successfully"}
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="Volunteer not found")



# Coordinator Endpoints

# Create a new coordinator
@app.post("/coordinators/")
async def create_coordinator(name: str, email: str):
    try:
        new_coordinator = Coordinator(name=name, email=email)
        new_coordinator.save()
        return {"message": "Coordinator created successfully", "coordinator": new_coordinator.to_dict()}
    except ValidationError as e:
        return {"error": str(e)}

# Custom function to convert MongoDB document to dictionary
def to_dict(self):
    return {
        "id": str(self.id),
        "name": self.name,
        "email": self.email,
    }

# Add the to_dict function to the Coordinator class
Coordinator.to_dict = to_dict


@app.get("/coordinators/{coordinator_id}", response_model=CoordinatorResponse)
async def read_coordinator(coordinator_id: str = Path(..., description="Coordinator ID")):
    try:
        coordinator = Coordinator.objects.get(id=coordinator_id)
        # Create a CoordinatorResponse object with the necessary fields
        response_data = {
            "id": str(coordinator.id),  # Convert ObjectId to string
            "name": coordinator.name,
            "email": coordinator.email,
        }
        return response_data
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="Coordinator not found")

Coordinator.to_dict = to_dict


@app.put("/coordinators/{coordinator_id}", response_model=CoordinatorResponse)
async def update_coordinator(
    coordinator_id: str,
    updated_coordinator: CoordinatorCreate
):
    try:
        coordinator = Coordinator.objects.get(id=coordinator_id)
        coordinator.update(**updated_coordinator.dict())
        return coordinator
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="Coordinator not found")

@app.delete("/coordinators/{coordinator_id}", response_model=dict)
async def delete_coordinator(coordinator_id: str = Path(..., description="Coordinator ID")):
    try:
        coordinator = Coordinator.objects.get(id=coordinator_id)
        coordinator.delete()
        return {"message": "Coordinator deleted successfully"}
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="Coordinator not found")

# VolunteerProject Endpoints

def convert_to_response_model(project: VolunteerProject):
    return VolunteerProjectResponse(
        id=str(project.id),
        name=project.name,
        description=project.description,
        start_date=project.start_date,
        end_date=project.end_date,
        coordinator=str(project.coordinator.id),  # Extract the coordinator's ID as a string
    )

@app.post("/volunteer-projects/", response_model=VolunteerProjectResponse)
async def create_volunteer_project(project: VolunteerProjectCreate):
    new_project = VolunteerProject(**project.dict())
    new_project.save()
    
    # Convert the new project to the response model
    response_project = convert_to_response_model(new_project)
    
    return response_project

@app.get("/volunteer-projects/{project_id}", response_model=VolunteerProjectResponse)
async def read_volunteer_project(project_id: str = Path(..., description="Project ID")):
    try:
        project = VolunteerProject.objects.get(id=project_id)
        response_project = VolunteerProjectResponse(
            id=str(project.id),  # Convert the ObjectId to a string
            name=project.name,
            description=project.description,
            start_date=project.start_date,
            end_date=project.end_date,
            coordinator=str(project.coordinator.id),  # Convert the coordinator's ObjectId to a string
        )
        return response_project
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="Project not found")


@app.delete("/volunteer-projects/{project_id}", response_model=dict)
async def delete_volunteer_project(project_id: str = Path(..., description="Project ID")):
    try:
        project = VolunteerProject.objects.get(id=project_id)
        project.delete()
        return {"message": "Project deleted successfully"}
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="Project not found")


# ProjectReservation Endpoints

@app.post("/project-reservations/", response_model=ProjectReservationResponse)
async def create_project_reservation(reservation: ProjectReservationCreate):
    new_reservation

# Authentication
def authenticate_user(email: str, password: str):
    # Find the user in the database based on the provided email
    user = db.volunteers.find_one({"email": email})
    if user and verify_password(password, user["password"]):
        return user

# Password Hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# JWT Token
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Login Endpoint
@app.post("/login/")
async def login_for_access_token(user: UserLogin):
    db_user = authenticate_user(user.email, user.password)
    if not db_user:
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}




