# HNG User Authentication and Organization Project

## Description

This project implements a Flask application with user authentication and organization management. Users can register, log in, and manage organizations they create or belong to. The application uses a PostgreSQL database and provides endpoints for user and organization operations.

## Setup

1. Create a virtual environment and activate it:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

2. Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Set up the environment variables in the `.env` file:
    ```
    DATABASE_URI=postgresql://username:password@localhost/dbname
    JWT_SECRET_KEY=your_jwt_secret_key
    ```

4. Run the migrations to set up the database schema:
    ```bash
    flask db init
    flask db migrate -m "Initial migration"
    flask db upgrade
    ```

5. Run the application:
    ```bash
    python run.py
    ```

## Endpoints

- `POST /auth/register`: Register a new user.
- `POST /auth/login`: Log in a user.
- `GET /api/users/<id>`: Get user details.
- `GET /api/organisations`: Get all organizations the user belongs to or created.
- `GET /api/organisations/<orgId>`: Get a single organization by ID.
- `POST /api/organisations/<orgId>/users`: Add a user to an organization.
