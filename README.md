# ATM Simple API

This is a simple ATM API developed with FastAPI and SQLModel to manage users, deposits, and withdrawals. **This application is designed to run exclusively using Docker.**

## Features

- **Create users**: Users can be created with a name, PIN, initial balance, and other details.
- **Retrieve users**: View a list of all registered users.
- **Make deposits**: Increase a user's balance via a bank account number.
- **Make withdrawals**: Decrease a user's balance if the correct PIN is provided and sufficient funds are available.
- **Database population**: The application automatically populates the database with 50 test users if it is empty.

## Requirements

- **Docker**: The application is configured to run inside a Docker container with PostgreSQL as the database.

## Installation and Execution

### Step 1: Clone the repository

Clone this repository to your local machine:

```bash
git clone https://github.com/Urielglb/Backend_HW_Project-.git
cd Backend_HW_Project
```

### Step 2: Configure the `.env` file

In the root directory, create a file named `.env` and add the following content:

```env
DB_URL="postgresql://postgres:hw_example@postgresdb:5432"
BACKEND_CORS_ORIGIN="http://localhost:5173"
```

#### Breakdown of the `.env` file:

- **DB_URL**: The URL for connecting to the PostgreSQL database. The database is configured to run inside a Docker container named `postgresdb`, using the `postgres` user with the password `hw_example`. The database operates on port `5432`.

    ```env
    DB_URL="postgresql://postgres:hw_example@postgresdb:5432"
    ```

- **BACKEND_CORS_ORIGIN**: Specifies the allowed origin for CORS requests. In this case, the frontend application (e.g., a Vue or React interface) runs at `http://localhost:5173`, and this URL is set as the allowed origin for requests to the backend.

    ```env
    BACKEND_CORS_ORIGIN="http://localhost:5173"
    ```

### Step 3: Run the application with Docker

Build and run the Docker containers using Docker Compose:

```bash
docker-compose up --build
```

This will start both the FastAPI backend and the PostgreSQL database inside Docker containers. Once the containers are running, the application will be available at `http://localhost:8000`.

### Step 4: Access the API

- **API Base URL**: [http://localhost:8000](http://localhost:8000)
- **Swagger UI (Interactive API Documentation)**: [http://localhost:8000/docs](http://localhost:8000/docs)

Check out the complete documentation for available endpoints at:  
[http://localhost:8000/docs#/Users](http://localhost:8000/docs#/Users)

### Step 5: Shut down the application

To stop and shut down the application, run:

```bash
docker-compose down
```

To also remove the database, run:

```bash
docker-compose down -v
```