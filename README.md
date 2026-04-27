# 🛒 Ecommerce API (FastAPI + PostgreSQL)

A fully functional Ecommerce backend built using **FastAPI** and **PostgreSQL**, implementing core features like product management, cart system, and checkout flow.

---

## 🚀 Tech Stack

* **Backend Framework:** FastAPI
* **Database:** PostgreSQL
* **ORM:** SQLAlchemy
* **Validation:** Pydantic
* **Server:** Uvicorn

---

## 📂 Project Structure

```
ecommerce/
│
├── app/
│   ├── main.py              # Entry point
│   ├── database.py          # DB connection
│   │
│   ├── models.py            # SQLAlchemy models
│   │
│   ├── schemas.py           # Pydantic schemas
│   │
│   ├── routes/              # API routes
│   │   └── routes.py
│
├── .env
├── requirements.txt
├── .gitignore
└── README.md
```

---

## ⚙️ Setup Instructions

### 1️⃣ Clone Repository

```bash
git clone https://github.com/your-username/ecommerce-fastapi.git
cd ecommerce-fastapi
```

---

### 2️⃣ Create Virtual Environment

```bash
python -m venv myvenv
source myvenv/bin/activate   # Linux/Mac
myvenv\Scripts\activate      # Windows
```

---

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 4️⃣ Configure Environment Variables

Create `.env` file:

```env
DATABASE_URL=postgresql://postgres:password@localhost:5432/EcommerceFastAPI_db
```

---

### 5️⃣ Run Server

```bash
uvicorn app.main:app --reload
```

---

### 6️⃣ Open API Docs

👉 http://127.0.0.1:8000/docs

---

## 📦 Features

### 🛍️ Product Management

* Create product
* Get all products
* Get single product
* Update product (PUT & PATCH)
* Delete product

---

### 🛒 Cart System

* Add product to cart
* Remove product from cart
* View cart with total price
* Quantity management

---

### 💳 Checkout System

* Create order from cart
* Auto calculate total amount
* Clear cart after checkout

---

## 🔌 API Endpoints

### 🔹 Products

| Method | Endpoint             | Description        |
| ------ | -------------------- | ------------------ |
| GET    | `/api/products/`     | Get all products   |
| POST   | `/api/products/`     | Create product     |
| GET    | `/api/products/{id}` | Get single product |
| PUT    | `/api/products/{id}` | Update product     |
| PATCH  | `/api/products/{id}` | Partial update     |
| DELETE | `/api/products/{id}` | Delete product     |

---

### 🔹 Cart

| Method | Endpoint            | Description      |
| ------ | ------------------- | ---------------- |
| POST   | `/api/cart/add/`    | Add item to cart |
| POST   | `/api/cart/remove/` | Remove item      |
| GET    | `/api/cart/{id}`    | Get cart details |

---

### 🔹 Checkout

| Method | Endpoint         | Description   |
| ------ | ---------------- | ------------- |
| POST   | `/api/checkout/` | Checkout cart |

---

## 🧪 Example Request

### Add to Cart

```json
{
  "product_id": 1,
  "quantity": 2
}
```

---

### Checkout

```json
{
  "cart_id": 1
}
```

---

## 🧠 What You Learned

* FastAPI architecture
* SQLAlchemy ORM
* Pydantic validation
* REST API design
* Ecommerce flow (cart → checkout)

---

## 👨‍💻 Author

**Karan**
Python Developer

---

## ⭐ Support

If you like this project, give it a ⭐ on GitHub!
