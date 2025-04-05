# Ecommerce System API

## 📌 Overview

This project is a Django REST Framework (DRF) based API for managing products and their reviews. It provides authentication, product management, review handling, order management, and user management with JWT authentication.

## 📂 Features

### 🛠️ RESTful API with Django REST Framework (DRF)
- Full CRUD operations for Products, Reviews, and Orders.
- Supports filtering, searching, and pagination for products.
- Categorization for products.

### 🔑 JWT Authentication
- Secure authentication using JWT (JSON Web Token).
- Supports login via `/api/token/`, returning Access Token and Refresh Token.
- Users can refresh tokens via `/api/token/refresh/`.

### ✨ Reviews System
- Each product can have multiple reviews.
- Reviews are rated from 1 to 5.
- Reviews are linked using ForeignKey.
- Users can only modify/delete their own reviews.

### 💼 Order Management
- Users can create and manage orders.
- Orders are linked to users and products.
- Each order has a status (Pending, Shipped, Delivered, Canceled, RETURNED).
- Users can view their order history.
- Admins can update order statuses.

### 🔍 Filtering, Search & Pagination
- Search products by name, price, or brand.
- Filter products based on ratings and categories.
- Pagination support for large product datasets.

### 🐛 API Documentation
- Uses drf-spectacular for API documentation.
- Swagger UI is available at `/api/swagger/`.
- OpenAPI Schema can be accessed at `/api/schema/`.

### 📂 Modular Apps
- `product` app → Manages products.
- `review` app → Manages reviews.
- `order` app → Handles order processing.
- `account` app → Handles authentication & users.

### 📧 Password Reset via Email
- Forgot Password (`/api/forgot_password/`): Sends an email with a reset token.
- Reset Password (`/api/reset_password/<token>/`): Resets the password using the token sent via email.
- Email Sending is Configured using SMTP settings.

### 🚀 Performance & Security Enhancements
- Uses `select_related` and `prefetch_related` for optimized queries.
- Permissions ensure only authenticated users can manage orders and reviews.

## 🔗 API Endpoints

### Authentication (Account App)
| Method | Endpoint | Description |
|--------|---------|-------------|
| POST | `/api/register/` | Register a new user |
| GET | `/api/user/` | Get current user data |
| PUT | `/api/user/update/` | Update user details |
| POST | `/api/forgot_password/` | Request password reset email |
| POST | `/api/reset_password/<token>/` | Reset password with token |
| POST | `/api/token/` | Obtain JWT access and refresh token |
| POST | `/api/token/refresh/` | Refresh access token |

### Product Management (Product App)
| Method | Endpoint | Description |
|--------|---------|-------------|
| GET | `/api/products/` | Get all products (supports filtering, search & pagination) |
| GET | `/api/products/<pk>/` | Get product by ID |
| POST | `/api/products/new/` | Create a new product |
| PUT | `/api/products/update/<pk>/` | Update a product |
| DELETE | `/api/products/delete/<pk>/` | Delete a product |

### Order Management (Order App)
| Method | Endpoint | Description |
|--------|---------|-------------|
| GET | `/api/orders/user/orders/` | Get all orders for the logged-in user |
| GET | `/api/orders/user/orders/<pk>/` | Get order by ID |
| POST | `/api/orders/user/orders/create/` | Create a new order |
| GET | `/api/orders/admin/orders/` | Get all orders (Admin only) |
| PUT | `/api/orders/admin/orders/<pk>/process/` | Process an order (Admin only) |

### Reviews (Review App)
| Method | Endpoint | Description |
|--------|---------|-------------|
| POST | `/api/reviews/<pk>/reviews/` | Create or update a review for a product |
| DELETE | `/api/reviews/<pk>/reviews/delete/` | Delete a review |

### API Documentation
| Method | Endpoint | Description |
|--------|---------|-------------|
| GET | `/swagger/` | API Documentation (Swagger UI) |
| GET | `/schema/` | OpenAPI Schema |

## 🛠️ Setup & Installation

### 1️⃣ Clone the Repository
```sh
git clone https://github.com/Ahmad-Jaber0/Ecommerce.git
cd your-repo
```

### 2️⃣ Install Dependencies
```sh
pip install -r requirements.txt
```

### 3️⃣ Set Up the Database
```sh
python manage.py migrate
```

### 4️⃣ Create a Superuser (Optional)
```sh
python manage.py createsuperuser
```

### 5️⃣ Run the Server
```sh
python manage.py runserver
```

### 6️⃣ Test API Endpoints
Use Postman or Swagger UI (`/swagger/`) to interact with the API.

## 📧 SMTP Email Configuration (For Password Reset)
In `settings.py`, configure your email settings:
```python
EMAIL_HOST = 'your_smtp_host'
EMAIL_HOST_USER = 'your_email_user'
EMAIL_HOST_PASSWORD = 'your_email_password'
EMAIL_PORT = your_port
EMAIL_USE_TLS = True  # or False depending on your provider
EMAIL_USE_SSL = False  # or True depending on your provider
```
Make sure to replace these values with actual credentials or use environment variables.


## 💡 Future Enhancements
- Real-time order tracking.
- Integrate Stripe/PayPal for payments.
- Advanced analytics dashboard.

🚀 Developed with Django REST Framework. 