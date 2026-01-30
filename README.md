# Farmstack API & Web Application

Full‑stack web application built with a React (TypeScript) frontend, a FastAPI backend, and an Nginx reverse proxy.  
The application uses **MongoDB Atlas** as a cloud database and is fully containerized using **Docker Compose**.

This project is designed with clear architecture, reproducible setup, and documented API endpoints.

## In brief:

The project is fully reproducible using Docker Compose.

MongoDB Atlas is used as a managed cloud database.

Environment variables are handled securely via a template.

Swagger and FastAPI ReDoc UI provide full API documentation and testing.

The architecture follows production‑style best practices:

frontend served as static assets

backend isolated as an API service

reverse proxy for unified access

## Prerequisites

- Docker Desktop installed and running
- Docker Compose v2 (`docker compose`)
- A MongoDB Atlas account


## Overview

The application consists of:

- **Frontend**: React + TypeScript Single Page Application (SPA)
- **Backend**: FastAPI REST API
- **Database**: MongoDB Atlas
- **Reverse Proxy**: Nginx
- **Containerization**: Docker & Docker Compose

The backend exposes a REST API for authentication, list management, and item management.

## Tech Stack

- Frontend: React, TypeScript
- Backend: FastAPI (Python)
- Database: MongoDB Atlas
- Reverse Proxy: Nginx (Alpine)
- Containerization: Docker, Docker Compose

## Environment Configuration (MongoDB Atlas)

The backend connects to **MongoDB Atlas** using environment variables.

### Creating the `.env` file

A template is provided:

backend/.env.template

Before running the application:

```bash
cp backend/.env.template backend/.env
```

Edit backend/.env and provide your MongoDB Atlas credentials.


Example:

MongoDB connection
MONGO_URI=mongodb+srv://<dbuser>:<password>@cluster.mongodb.net/dbname?

JWT settings
JWT_SECRET=*************
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60

# Debug mode
DEBUG=false
###############################################################

The .env file is not committed to the repository.


## Running the Application

All commands must be executed from the project root directory

Build and start all services

```bash
docker compose up --build
```
This starts: 

Backend API
Frontend Build
Nginx server


## Accessing the Application

 Frontend 
 ```bash
 http://localhost 
 ```
 Served by Nginx
 
## API Documentation (Swagger) and (FastAPI ReDoc)

The backend provides Swagger UI via FastAPI

Swagger URL

```bash
http://localhost:8000/docs
```
Swagger is enabled by exposing the backend port in docker-compose.yaml:

ports:
  - "8000:8000"

ports:
  - "8000:8000"
 
FastAPI ReDoc could provide automatic generation of API documentation from OpenAPI specifications

FastAPI ReDoc URL
```markdown
http://localhost:8000/redoc
```

## API Endpoints

Authentication (/api/auth) - Handles user authentication.

- POST /api/auth/login

- POST /api/auth/register (if implemented)


Lists (/api/lists) - Manages user lists.

- GET /api/lists – Retrieve all lists

- POST /api/lists – Create a new list

- DELETE /api/lists/{list_id} – Delete a list


Items (/api/items) - Manages items within lists.

- POST /api/items – Create a new item

- PATCH /api/items/{item_id} – Update an item

- DELETE /api/items/{item_id} – Delete an item

## Backend Initialization

On application startup, MongoDB indexes are created automatically:

```bash
@app.on_event("startup")
async def startup_event():
    await create_indexes()
```
This ensures database performance and data integrity.

## Useful Docker Commands

Stop containers
```bash
docker compose down
```
Stop containers and remove volumes
```bash
docker compose down -v
```
View backend logs
```bash
docker logs backend
```
Restart build only for backend service, without using cache from previous builds
```bash
docker compose build --no-cache backend
```
Build  και start 
```bash
docker compose up --build
```
## Architecture Diagram Description

The system follows a three‑tier architecture consisting of a frontend layer, a backend API layer, and a database layer. All components are containerized and orchestrated using Docker Compose.

### Frontend Layer
The frontend is a Single Page Application (SPA) developed with React and TypeScript.
It is built into static assets and served by Nginx.
Handles user interaction and UI rendering
Communicates with the backend exclusively through HTTP requests
Does not access the database directly
All API calls are routed through the reverse proxy

### Reverse Proxy Layer (Nginx)
Nginx acts as a reverse proxy and static file server.
Serves the frontend static build
Forwards API requests to the backend service
Provides a single entry point for the application
Decouples frontend and backend networking
This layer improves scalability and mirrors a production‑style deployment.

### Backend Layer (FastAPI)
The backend is implemented using FastAPI and exposes a RESTful API.
Responsibilities include:
- Authentication and authorization
- Business logic for lists and items
- Data validation and request handling
- Database interaction

The backend is structured using modular routers:

/api/auth – authentication endpoints

/api/lists – list management

/api/items – item management

On application startup, database indexes are created automatically to ensure performance and data integrity.

### Database Layer (MongoDB Atlas)
The database layer uses MongoDB Atlas, a managed cloud‑based NoSQL database.
Stores application data (users, lists, items)
Accessed only by the backend service
Connection details are provided via environment variables
No database credentials are exposed to the frontend

### Containerization and Orchestration
All components are containerized using Docker and orchestrated with Docker Compose.
Each service runs in its own isolated container
Services communicate through a shared Docker network
Environment variables are injected using a .env file generated from a template
The architecture is fully reproducible on any system with Docker installed


## Πληροφορίες στα Ελληνικά 
Η εφαρμογή γίνεται deploy χρησιμοποιώντας Docker και Docker Compose, χωρίς να απαιτείται χειροκίνητη εγκατάσταση εξαρτήσεων στο σύστημα.
Όλα τα επιμέρους μέρη της εφαρμογής (frontend, backend, reverse proxy) εκτελούνται σε ξεχωριστά containers, τα οποία συντονίζονται μέσω ενός ενιαίου docker-compose.yml αρχείου.
Η διαδικασία deployment περιλαμβάνει τα εξής βήματα:
1. Δημιουργία του αρχείου περιβάλλοντος (.env) για το backend, βασισμένο στο παρεχόμενο template, με τα στοιχεία σύνδεσης στο MongoDB Atlas.
2. Εκτέλεση της εντολής: ```bash docker compose up --build```
3. Το Docker: χτίζει τα images για frontend και backend, ξεκινά τα containers, ρυθμίζει την εσωτερική επικοινωνία των services
4. Το frontend σερβίρεται μέσω Nginx, ενώ το backend API είναι διαθέσιμο μέσω HTTP.
5. Η εφαρμογή είναι έτοιμη προς χρήση μέσω browser, ενώ το API μπορεί να ελεγχθεί μέσω Swagger UI ή FastAPI ReDoc
6. Κατά την πρώτη είσοδο ο χρήστης της εφαρμογής πρέπει να επιλεξει την επιλογη "Register" και να κλανει εγγραφή.
7. Το email πρέπει να συμπληρωθεί σε έγκυρη φόρμα ηλεκτρονικου ταχυδρομείου και το password πρέπει να είναι τουλάχιστον 8 χαρακτήρες.
8. Μετά την εγγραφή ο χρήστης εισέρχεται κανονικά με "Login" στην εφαρμογή.

