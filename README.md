<div align="center">

# **Grocery Store**
## Full-Stack Django E-Commerce Platform

*A production-ready multi-store grocery e-commerce application with real-time geolocation, role-based access control, and a complete shopping workflow.*

### **Technology Stack**

[![Python](https://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Django](https://img.shields.io/badge/Django-5.2-092E20?style=for-the-badge&logo=django&logoColor=white)](https://www.djangoproject.com)
[![SQLite](https://img.shields.io/badge/SQLite-3-003B57?style=for-the-badge&logo=sqlite&logoColor=white)](https://www.sqlite.org)
[![Bootstrap](https://img.shields.io/badge/Bootstrap-5.2-7952B3?style=for-the-badge&logo=bootstrap&logoColor=white)](https://getbootstrap.com)

[![Azure Pipelines](https://img.shields.io/badge/Azure_Pipelines-CI%2FCD-2560E0?style=for-the-badge&logo=azurepipelines&logoColor=white)](https://azure.microsoft.com/en-us/products/devops/pipelines)
[![Azure App Service](https://img.shields.io/badge/Azure_App_Service-Deployed-0078D4?style=for-the-badge&logo=microsoftazure&logoColor=white)](https://azure.microsoft.com/en-us/products/app-service)
[![Gunicorn](https://img.shields.io/badge/Gunicorn-WSGI-499848?style=for-the-badge&logo=gunicorn&logoColor=white)](https://gunicorn.org)

</div>

---

## Overview

A Django-based e-commerce platform that models real-world grocery retail with **multi-store inventory management**, where each store maintains independent stock levels for every product. Customers can browse products, find their nearest store via geolocation, add items to a store-scoped cart, and complete a full checkout flow with address and payment collection.

The application features a **custom admin dashboard** for staff to manage users and orders, a **role-based access system** that restricts inventory visibility by store assignment, and a **CI/CD pipeline** deploying to Azure App Service.

---

## Features

### **Shopping Experience**
- **Advanced Product Filtering** — keyword search, category dropdown, price range, in-stock filter with 6 sort modes and configurable pagination (12–60 items/page)
- **Filter Persistence** — filters saved to session and restored on revisit, with removable filter chips
- **Store-Aware Cart** — cart is scoped to a selected store; changing stores clears the cart to prevent cross-store ordering
- **Two-Step Checkout** — address collection followed by payment entry, with order confirmation
- **Per-Store Stock Display** — product detail pages show availability at each store location

### **Store Locator & Geolocation**
- **Find My Closest Store** — enter a postcode to find the nearest store using the Haversine formula
- **Automatic Geocoding** — store coordinates are auto-populated via a Django `pre_save` signal when a postcode is set
- **Google Maps Integration** — store addresses link directly to Google Maps

### **User Management**
- **Custom User Model** — extends Django's `AbstractUser` with store association for staff
- **Profile Dashboard** — view active/past orders, manage payment methods, edit profile
- **Secure Auth** — registration with email uniqueness validation, alphabetic-only name enforcement, session-preserving password changes

### **Admin & Staff Tools**
- **Custom Admin Dashboard** — staff-only interface for user management (activate/deactivate, grant/revoke staff), order management (filter by user, update status), and account creation with role selection
- **Role-Based Inventory** — staff see only products for their assigned store in Django admin; superusers see all
- **Order Lifecycle** — Active → Completed / Cancelled with automatic stock adjustment on placement

---

## System Architecture

```mermaid
graph TB
    subgraph "Frontend"
        UI[Bootstrap 5 UI<br/>Django Templates]
    end

    subgraph "Django Application"
        VIEWS[Views Layer<br/>Request Handling]
        SERVICES[Service Layer<br/>Business Logic]
        UTILS[Utilities<br/>Geocoding & Filtering]
        MODELS[Model Layer<br/>ORM & Signals]
    end

    subgraph "External Services"
        GEO[geocode.maps.co<br/>Geocoding API]
        AZURE[Azure App Service<br/>Production Host]
    end

    subgraph "Data"
        DB[(SQLite<br/>Database)]
    end

    UI -->|HTTP Requests| VIEWS
    VIEWS -->|Order Creation| SERVICES
    VIEWS -->|Product Filters| UTILS
    UTILS -->|Postcode Lookup| GEO
    SERVICES --> MODELS
    VIEWS --> MODELS
    MODELS -->|ORM| DB

    style UI fill:#7952B3,stroke:#6f42c1,color:#fff
    style VIEWS fill:#092E20,stroke:#0c4b33,color:#fff
    style SERVICES fill:#092E20,stroke:#0c4b33,color:#fff
    style UTILS fill:#092E20,stroke:#0c4b33,color:#fff
    style MODELS fill:#092E20,stroke:#0c4b33,color:#fff
    style GEO fill:#4285F4,stroke:#3367d6,color:#fff
    style AZURE fill:#0078D4,stroke:#005ba1,color:#fff
    style DB fill:#003B57,stroke:#00567a,color:#fff
```

### **Shopping Flow**

```mermaid
sequenceDiagram
    participant C as Customer
    participant V as Views
    participant S as Service Layer
    participant DB as Database

    C->>V: Browse products (filter/sort/search)
    V->>DB: Query with filters & pagination
    DB-->>V: Filtered product list
    V-->>C: Render product catalog

    C->>V: Select store & add to cart
    V->>DB: Validate stock at store
    DB-->>V: Stock available
    V->>DB: Create/update CartEntry
    V-->>C: Cart updated

    C->>V: Checkout (address → payment)
    V-->>C: Collect shipping & payment info

    C->>V: Confirm order
    V->>S: create_order_from_cart()
    S->>DB: Create Order + OrderItems
    S->>DB: Reduce store stock
    S->>DB: Clear cart
    S-->>V: Order created
    V-->>C: Order confirmation page
```

---

## Database Schema

```mermaid
erDiagram
    Category ||--o{ Product : contains
    Product ||--o{ PerStoreProduct : "stocked at"
    Store ||--o{ PerStoreProduct : "carries"
    Store ||--|| StoreOpeningHours : has
    CustomUser ||--o{ Cart : owns
    Cart ||--o{ CartEntry : contains
    CartEntry }o--|| PerStoreProduct : references
    CustomUser ||--o{ Order : places
    Order ||--o{ OrderItem : contains
    OrderItem }o--|| Product : "is a"
    CustomUser ||--o{ Address : has
    CustomUser ||--o{ Payment : has
    Order }o--o| Address : "ships to"
    Order }o--o| Payment : "paid with"
    CustomUser }o--o| Store : "assigned to"

    Product {
        int id PK
        string name
        string description
        decimal price
        int quantity
        string image_url
        datetime created_at
        int category_id FK
    }

    PerStoreProduct {
        int id PK
        int product_id FK
        int store_id FK
        int quantity
    }

    Store {
        int id PK
        string name
        string address
        string postcode
        string phone_number
        float latitude
        float longitude
    }

    Order {
        int id PK
        int user_id FK
        string status
        decimal total
        datetime created_at
    }
```

---

## Quick Start

### **Prerequisites**
```bash
python --version  # Python 3.10+
```

### **Setup**
```bash
# Clone the repository
git clone https://github.com/Brycekoh/grocery-store.git
cd grocery-store

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### **Database**
```bash
python manage.py makemigrations
python manage.py migrate
```

### **Seed Sample Data**
```bash
python manage.py seed
```
> Populates the database with 8 categories, 24 products, 3 stores (with opening hours), and randomized inventory across all stores. Use `--clear` to reset before seeding.

### **Create Admin User**
```bash
python manage.py createsuperuser
```

### **Run**
```bash
python manage.py runserver
```

### **Access**
- **Main Site:** http://127.0.0.1:8000/
- **Admin Dashboard:** http://127.0.0.1:8000/admin-dashboard/ (staff only)
- **Django Admin:** http://127.0.0.1:8000/admin/

### **Run Tests**
```bash
python manage.py test
```

---

## API Routes

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| `GET` | `/` | Product catalog (home) | No |
| `GET` | `/products` | Product listing with filters | No |
| `GET` | `/product/<id>` | Product detail with store stock | No |
| `POST` | `/product/<id>/select_store` | Set active store for product | Yes |
| `GET` | `/stores` | Store directory with geolocation | No |
| `GET/POST` | `/cart` | View/update cart | Yes |
| `POST` | `/add_cart` | Add item to cart | Yes |
| `GET/POST` | `/checkout_address` | Shipping address step | Yes |
| `GET/POST` | `/checkout_payment` | Payment step | Yes |
| `GET` | `/confirm` | Order confirmation | No |
| `GET` | `/order/<id>` | Order detail | Yes |
| `GET/POST` | `/signup/` | User registration | No |
| `GET` | `/profile/` | User profile dashboard | Yes |
| `GET/POST` | `/profile/edit/` | Edit profile | Yes |
| `POST` | `/profile/payment/add/` | Add payment method | Yes |
| `POST` | `/profile/payment/edit/` | Edit payment method | Yes |
| `POST` | `/profile/payment/remove/` | Remove payment method | Yes |
| `GET` | `/admin-dashboard/` | Staff admin dashboard | Staff |

---

## CI/CD Pipeline

The project uses **Azure Pipelines** with a two-stage deployment:

```mermaid
flowchart LR
    subgraph "Stage 1: Build"
        A[Install Dependencies] --> B[Run Migrations]
        B --> C[Run Test Suite]
        C --> D[Publish Artifact]
    end

    subgraph "Stage 2: Deploy"
        D --> E[Download Artifact]
        E --> F[Deploy to Azure<br/>App Service]
    end

    style A fill:#2560E0,stroke:#1a4bb8,color:#fff
    style B fill:#2560E0,stroke:#1a4bb8,color:#fff
    style C fill:#2560E0,stroke:#1a4bb8,color:#fff
    style D fill:#2560E0,stroke:#1a4bb8,color:#fff
    style E fill:#0078D4,stroke:#005ba1,color:#fff
    style F fill:#0078D4,stroke:#005ba1,color:#fff
```

---

## Testing

15 unit and integration tests covering:

| Test Suite | Coverage |
|------------|----------|
| `test_cart.py` | Cart quantity validation, add/remove items, stock limit enforcement |
| `test_forms.py` | User registration form validation (email uniqueness, name format) |
| `test_list_of_stores.py` | Geolocation closest-store calculation with mocked geocoding |
| `test_order_creation.py` | End-to-end order creation from cart |
| `test_product_view.py` | Product filtering, sorting, pagination, search |

---

## License

MIT License — See [LICENSE](LICENSE) for details.
