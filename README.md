# ToDo List Backend

## Project Description

This is the backend for a ToDo List application. It allows users to register, log in, manage tasks, and perform CRUD operations on their to-do items. The backend is built using FastAPI, with PostgreSQL for data storage, and JWT (JSON Web Token) for user authentication.

## Tech Stack

- **Backend**: FastAPI (Python)
- **Authentication**: JWT (JSON Web Token)
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Libraries**: 
  - `fastapi`
  - `uvicorn` (ASGI server)
  - `sqlalchemy` (ORM for database interaction)
  - `python-dotenv` (to manage environment variables)
  - `psycopg2` (PostgreSQL database adapter)
  - `PyJWT` (for JWT encoding and decoding)
  - `passlib` (for password hashing)
  - `bcrypt` (for stronger password hashing)
  - `python-jose` (for JWT creation and validation)

## Prerequisites

1. **Python 3.7+**
2. **PostgreSQL** (Ensure it’s installed and configured on your machine)

## Routes

- **GET /task**: Retrieve all tasks (requires authentication).
- **GET /task/{id}**: Retrieve a task by ID (requires authentication).
- **POST /task**: Create a new task (requires authentication).
- **PUT /task/{id}**: Update a task by ID (requires authentication).
- **DELETE /task/{id}**: Delete a task by ID (requires authentication).
- **POST /auth/register**: Register a new user.
- **POST /auth/login**: Log in with credentials and receive a JWT.
