# 🛒 Ecommerce FastAPI Backend

A production-style Ecommerce Backend built with **FastAPI**, **PostgreSQL**, **SQLAlchemy Async**, **Alembic**, **JWT Authentication**, **AWS S3**, **CloudFront**, and **Docker**.

This project follows a modular, service-oriented architecture and demonstrates real-world backend development practices including authentication, product management, image uploads, cart management, pagination, filtering, soft deletion, Dockerization, and database migrations.

---

# 🚀 Features

## Authentication

- User Registration
- User Login
- JWT Access Token
- JWT Refresh Token
- Protected APIs
- Password Hashing
- Role-Based Architecture Ready

---

## Product Management

- Create Product
- Get Product List
- Get Single Product
- Update Product
- Soft Delete Product
- Pagination
- Sorting
- Stock Management
- Product Image Upload

---

## Cart Management

- Add Product To Cart
- Update Cart Quantity
- Reduce Quantity
- Remove Product From Cart
- Stock Validation
- Quantity Validation
- Cart Total Calculation
- Multiple Products Per User Cart

---

## Image Uploads

- AWS S3 Integration
- CloudFront CDN Integration
- Public Image URLs
- Optimized Image Delivery

---

## Database

- PostgreSQL
- Async SQLAlchemy
- Alembic Migrations
- Relationships
- UUID Primary Keys
- Soft Delete Support

---

## Docker Support

- Dockerized FastAPI Application
- Dockerized PostgreSQL
- Docker Compose
- Persistent Database Volumes
- Environment Variable Configuration
- Container Networking

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
- Docker Compose

---

# 📂 Project Structure

```text
Ecommerce Postgresql/
│
├── alembic/
│   ├── versions/
│
├── src/
│   │
│   ├── database/
│   │   ├── db_config.py
│   │   ├── config.py
│   │   ├── dependencies.py
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
├── .env
├── .dockerignore
├── .gitignore
├── alembic.ini
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
│
└── README.md
```

---

# ⚙️ Environment Variables

Create a `.env` file in the project root.

```env
# DATABASE

DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=db
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

---

# 🐳 Docker Setup

## Clone Repository

```bash
git clone <repository-url>
cd Ecommerce-Postgresql
```

---

## Start Containers

```bash
docker compose up --build -d
```

---

## Verify Running Containers

```bash
docker ps
```

Expected:

```text
ecommerce_app
ecommerce_db
```

---

## Run Database Migrations

```bash
docker exec -it ecommerce_app alembic upgrade head
```

---

## Open Swagger Docs

```text
http://localhost:8000/docs
```

---

# 🗄️ PostgreSQL Connection

If connecting through pgAdmin:

| Field | Value |
|---------|---------|
| Host | localhost |
| Port | 5555 |
| Username | postgres |
| Password | your_password |
| Database | Ecommerce_CompanyArc_DB |

---

# 📦 Docker Hub Image

Pull image directly:

```bash
docker pull karn21/ecommerce-fastapi:latest
```

---

# 🔄 Development Workflow

## Start Project

```bash
docker compose up -d
```

---

## View Logs

Application Logs:

```bash
docker logs -f ecommerce_app
```

Database Logs:

```bash
docker logs -f ecommerce_db
```

---

## Stop Project

```bash
docker compose down
```

---

## Rebuild Project

```bash
docker compose down

docker compose up --build -d
```

---

# 🧪 API Testing

Swagger UI:

```text
http://localhost:8000/docs
```

All APIs can be tested directly from Swagger.

---

# 🔐 Authentication Flow

## Register User

```text
POST /auth/register
```

---

## Login User

```text
POST /auth/login
```

Returns:

```json
{
  "access_token": "...",
  "refresh_token": "..."
}
```

---

## Authorize Requests

Click:

```text
Authorize
```

inside Swagger UI and provide:

```text
Bearer <access_token>
```

---

# 📸 Product Image Upload Flow

```text
Client
    ↓
FastAPI
    ↓
AWS S3
    ↓
CloudFront
    ↓
Public Image URL
```

---

# 🛒 Cart Flow

```text
User
    ↓
Add Product To Cart
    ↓
Stock Validation
    ↓
Cart Item Created
    ↓
Update Quantity
    ↓
Remove Product
```

---

# 📊 Current Features Completed

- Authentication Module
- JWT Authentication
- Product CRUD
- Product Pagination
- Product Sorting
- Product Filters
- AWS S3 Upload
- CloudFront Integration
- Cart Management
- Stock Validation
- Dockerization
- PostgreSQL Integration
- Alembic Migrations

---

# 🧹 Useful Docker Commands

## Show Running Containers

```bash
docker ps
```

---

## Show All Containers

```bash
docker ps -a
```

---

## Enter Application Container

```bash
docker exec -it ecommerce_app bash
```

---

## Restart Application

```bash
docker restart ecommerce_app
```

---

## Stop Containers

```bash
docker compose down
```

---

## Remove Containers & Volumes

```bash
docker compose down -v
```

⚠️ Warning: This deletes database data permanently.

---

# 👨‍💻 Author

**Karan**

FastAPI | PostgreSQL | Docker | AWS | Backend Development
