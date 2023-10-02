# Volunteering Application with FastAPI and MongoDB

This is a FastAPI application for managing volunteering activities. Users can add volunteers, delete volunteers, add projects, add project coordinators, and delete coordinators. The application uses MongoDB as its database.

## Features

- **Volunteer Management**
  - Add volunteers with details such as name, contact information, and skills.
  - Delete volunteers when they are no longer active.

- **Project Management**
  - Add projects with details like project name, description, and start/end dates.
  - Assign project coordinators to projects.
  - Remove project coordinators when needed.

## Installation

To run this application, you need to have Python and MongoDB installed on your system. Follow these steps to set up and run the application:

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/volunteer-fastapi.git


## Endpoints
Volunteers:

GET /volunteers: Get a list of all volunteers.
POST /volunteers: Add a new volunteer.
DELETE /volunteers/{volunteer_id}: Delete a volunteer by ID.
Projects:

GET /coordinators: Get a list of all projects.
POST /coordinators: Add a new project.
POST /coordinators/{project_id}/coordinators: Add a coordinator to a project.
DELETE /coordinators/{project_id}/coordinators/{coordinator_id}: Remove a coordinator from a project.

