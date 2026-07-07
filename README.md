# 🛒 Ecommerce FastAPI Backend

A production-style Ecommerce Backend built using **FastAPI**, **PostgreSQL**, **SQLAlchemy Async**, **Alembic**, **JWT Authentication**, **AWS S3**, **CloudFront**, and **Docker**.

This project follows a modular, service-oriented architecture inspired by real-world backend development practices. It demonstrates authentication, product management, image uploads, cart management, pagination, filtering, sorting, soft deletion, Dockerization, and database migrations.

---

# 🚀 Features

## 🔐 Authentication

- User Registration
- User Login
- JWT Access Token
- JWT Refresh Token
- Protected APIs
- Password Hashing (bcrypt)
- Role-Based Architecture Ready

---

## 🛍️ Product Management

- Create Product
- Get Product List
- Get Single Product
- Update Product
- Soft Delete Product
- Pagination
- Sorting
- Filtering
- Stock Management
- Product Image Upload

---

## 🛒 Cart Management

- Add Product To Cart
- Update Cart Quantity
- Reduce Quantity
- Remove Product From Cart
- Quantity Validation
- Stock Validation
- Cart Total Calculation
- Multiple Products Per User

---

## 🖼️ Image Uploads

- AWS S3 Integration
- CloudFront CDN Integration
- Public Image URLs
- Optimized Image Delivery

---

## 🗄️ Database

- PostgreSQL
- Async SQLAlchemy
- Alembic Migrations
- UUID Primary Keys
- Model Relationships
- Soft Delete Support

---

## 🐳 Docker

- Single Docker Image Architecture
- Dockerized FastAPI Application
- External PostgreSQL Connection
- Environment Variable Configuration
- Portable Deployment Workflow

---

# 🛠️ Tech Stack

## Backend
- FastAPI
- Python 3.12

## Database
- PostgreSQL
- SQLAlchemy Async
- Alembic

## Authentication
- JWT
- Passlib
- Bcrypt

## Storage
- AWS S3
- CloudFront

## Deployment
- Docker
- Docker Hub

---

# 📂 Project Structure

```text
Ecommerce Postgresql/
│
├── alembic/
│   ├── versions/
│   └── env.py
│
├── src/
│   │
│   ├── database/
│   │   ├── config.py
│   │   ├── db_config.py
│   │   ├── dependencies.py
│   │   ├── jwt_handler.py
│   │   └── models/
│   │
│   ├── services/
│   │   ├── auth/
│   │   ├── product/
│   │   └── cart/
│   │
│   ├── urls/
│   │
│   ├── utils/
│   │
│   └── main.py
│
├── .env.example
├── .dockerignore
├── .gitignore
├── alembic.ini
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

---

# ⚙️ Prerequisites

Before running the project, make sure you have installed:

- Python 3.12+
- PostgreSQL
- Docker
- Git

---

# ⚙️ Environment Variables

Create a `.env` file by copying the example file:

```bash
cp .env.example .env
```

Update the values according to your local environment:

```env
# DATABASE

DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=host.docker.internal
DB_PORT=5432
DB_NAME=Ecommerce_CompanyArc_DB

# JWT

SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
REFRESH_TOKEN_EXPIRE_DAYS=7

# AWS S3

AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
AWS_REGION=ap-south-1
AWS_BUCKET_NAME=your_bucket_name

# CLOUDFRONT

CLOUDFRONT_URL=https://your-cloudfront-url
```

> **Note:**  
> The FastAPI application runs inside Docker, while PostgreSQL runs on the host machine.  
> The application connects to the host database using `host.docker.internal`.

---

# 🗄️ Database Setup

## Create Database

Open PostgreSQL and create a database:

```sql
CREATE DATABASE Ecommerce_CompanyArc_DB;
```

## Run Database Migrations

After configuring `.env`, execute:

```bash
alembic upgrade head
```

Alembic will automatically create all required tables.

---

# 🐳 Docker Setup

## Clone Repository

```bash
git clone https://github.com/karankharvar2004/Ecommerce_FastAPI_Postgresql.git
cd Ecommerce_FastAPI_Postgresql
```

---

## Build and Run

```bash
docker compose up --build
```

Or run in detached mode:

```bash
docker compose up --build -d
```

---

## Verify Running Container

```bash
docker ps
```

Expected output:

```text
CONTAINER ID   IMAGE            PORTS                    NAMES
xxxxxxxxxxxx   ecommerce_app    0.0.0.0:8000->8000/tcp   ecommerce_app
```

---

# 🚀 Access API Documentation

Swagger UI:

```
http://localhost:8000/docs
```

ReDoc:

```
http://localhost:8000/redoc
```

---

# 🔌 API Modules

## Authentication

| Method | Endpoint | Description |
|----------|------------------|----------------|
| POST | `/auth/register` | Register User |
| POST | `/auth/login` | Login User |

---

## Products

| Method | Endpoint | Description |
|----------|------------------------|----------------------|
| POST | `/product/create` | Create Product |
| GET | `/product/list` | Product List |
| GET | `/product/{id}` | Get Single Product |
| PUT | `/product/{id}` | Update Product |
| DELETE | `/product/{id}` | Soft Delete Product |

---

## Cart

| Method | Endpoint | Description |
|----------|----------------------|----------------------|
| POST | `/cart/add` | Add Product To Cart |
| PATCH | `/cart/update` | Update Cart Quantity |
| DELETE | `/cart/remove` | Remove Product |
| GET | `/cart/list` | Get Cart Details |

---

# 🔐 Authentication Flow

## 1. Register User

```text
POST /auth/register
```

## 2. Login User

```text
POST /auth/login
```

Response:

```json
{
    "access_token": "...",
    "refresh_token": "..."
}
```

## 3. Authorize Swagger

Click the **Authorize** button and enter:

```text
Bearer <access_token>
```

---

# 📸 Product Image Upload Flow

```text
Client
   │
   ▼
FastAPI
   │
   ▼
AWS S3
   │
   ▼
CloudFront
   │
   ▼
Public Image URL
```

---

# 🛒 Cart Workflow

```text
User
   │
   ▼
Add Product
   │
   ▼
Stock Validation
   │
   ▼
Cart Updated
   │
   ▼
Quantity Update / Remove Product
   │
   ▼
Cart Total Calculation
```

---

# 🏗️ Deployment Architecture

```text
                 Docker Hub
                      │
                      ▼
         +---------------------------+
         |   FastAPI Docker Image    |
         +-------------+-------------+
                       │
          host.docker.internal
                       │
                       ▼
         +---------------------------+
         | PostgreSQL (Host Machine) |
         |      + pgAdmin            |
         +---------------------------+
```

### Workflow

1. Clone repository.
2. Create PostgreSQL database.
3. Copy `.env.example` to `.env`.
4. Configure environment variables.
5. Run `alembic upgrade head`.
6. Start Docker container.
7. Open Swagger and test APIs.

---

# 📦 Docker Hub

Pull the latest application image:

```bash
docker pull karn21/ecommerce-fastapi:latest
```

Run the container:

```bash
docker run --env-file .env -p 8000:8000 karn21/ecommerce-fastapi:latest
```

---

# 🔄 Development Workflow

## Start

```bash
docker compose up -d
```

## View Logs

```bash
docker logs -f ecommerce_app
```

## Stop

```bash
docker compose down
```

## Rebuild

```bash
docker compose down
docker compose up --build -d
```

---

# 🧪 Local Development

Run without Docker:

```bash
source venv/bin/activate

pip install -r requirements.txt

alembic upgrade head

uvicorn src.main:app --reload
```

---

# 📊 Current Features Completed

- ✅ Authentication Module
- ✅ JWT Authentication
- ✅ Product CRUD
- ✅ Product Pagination
- ✅ Product Sorting
- ✅ Product Filtering
- ✅ AWS S3 Upload
- ✅ CloudFront Integration
- ✅ Cart Management
- ✅ Stock Validation
- ✅ Dockerized FastAPI Application
- ✅ External PostgreSQL Integration
- ✅ Alembic Database Migrations

---

# 🧹 Useful Docker Commands

## Build Image

```bash
docker build -t ecommerce-fastapi .
```

## Start Project

```bash
docker compose up --build
```

## Running Containers

```bash
docker ps
```

## View Logs

```bash
docker logs -f ecommerce_app
```

## Stop Project

```bash
docker compose down
```

## Pull Latest Docker Hub Image

```bash
docker pull karn21/ecommerce-fastapi:latest
```

---

# 👨‍💻 Author

**Karan Kharvar**

**Python Backend Developer**  
FastAPI • PostgreSQL • Docker • AWS S3 • CloudFront • SQLAlchemy • Alembic

GitHub: https://github.com/karankharvar2004

---