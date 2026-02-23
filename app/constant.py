"""Constants and configuration for the minirm application."""

from pathlib import Path
from typing import Dict, List

HOME_DIR = str(Path.home())
APP_NAME = "squilio"
CONFIG_DIR = Path.home() / f".{APP_NAME}"

SCHEMAS: Dict[str, List[Dict[str, str]]] = {
    "users": [
        {"column": "id", "type": "INTEGER", "constraints": "PRIMARY KEY AUTOINCREMENT"},
        {"column": "name", "type": "VARCHAR(100)", "constraints": "NOT NULL"},
        {"column": "email", "type": "VARCHAR(100)", "constraints": "NOT NULL UNIQUE"},
        {"column": "phone", "type": "VARCHAR(20)", "constraints": "NULL"},
        {"column": "age", "type": "INTEGER", "constraints": "NULL"},
        {"column": "country", "type": "VARCHAR(50)", "constraints": "NULL"},
        {"column": "city", "type": "VARCHAR(50)", "constraints": "NULL"},
    ],
    "departments": [
        {"column": "id", "type": "INTEGER", "constraints": "PRIMARY KEY AUTOINCREMENT"},
        {"column": "name", "type": "VARCHAR(100)", "constraints": "NOT NULL"},
        {"column": "location", "type": "VARCHAR(100)", "constraints": "NOT NULL"},
    ],
    "employees": [
        {"column": "id", "type": "INTEGER", "constraints": "PRIMARY KEY AUTOINCREMENT"},
        {"column": "name", "type": "TEXT", "constraints": "NOT NULL"},
        {"column": "email", "type": "TEXT", "constraints": "NOT NULL UNIQUE"},
        {
            "column": "department_id",
            "type": "INTEGER",
            "constraints": "FK -> departments(id)",
        },
        {
            "column": "manager_id",
            "type": "INTEGER",
            "constraints": "FK -> employees(id)",
        },
        {"column": "salary", "type": "NUMERIC(10,2)", "constraints": "NULL"},
        {"column": "hire_date", "type": "DATE", "constraints": "NULL"},
    ],
    "categories": [
        {"column": "id", "type": "INTEGER", "constraints": "PRIMARY KEY AUTOINCREMENT"},
        {"column": "name", "type": "VARCHAR(50)", "constraints": "NOT NULL"},
        {"column": "description", "type": "TEXT", "constraints": "NOT NULL"},
    ],
    "suppliers": [
        {"column": "id", "type": "INTEGER", "constraints": "PRIMARY KEY AUTOINCREMENT"},
        {"column": "name", "type": "TEXT", "constraints": "NOT NULL"},
        {"column": "country", "type": "TEXT", "constraints": "NOT NULL"},
        {"column": "contact_email", "type": "TEXT", "constraints": "NOT NULL"},
    ],
    "products": [
        {"column": "id", "type": "INTEGER", "constraints": "PRIMARY KEY AUTOINCREMENT"},
        {"column": "name", "type": "VARCHAR(100)", "constraints": "NOT NULL"},
        {"column": "description", "type": "TEXT", "constraints": "NULL"},
        {
            "column": "category_id",
            "type": "INTEGER",
            "constraints": "FK -> categories(id) NOT NULL",
        },
        {
            "column": "supplier_id",
            "type": "INTEGER",
            "constraints": "FK -> suppliers(id) NOT NULL",
        },
        {"column": "price", "type": "NUMERIC(10,2)", "constraints": "NOT NULL"},
        {"column": "stock", "type": "INTEGER", "constraints": "NOT NULL"},
    ],
    "orders": [
        {"column": "id", "type": "INTEGER", "constraints": "PRIMARY KEY AUTOINCREMENT"},
        {
            "column": "user_id",
            "type": "INTEGER",
            "constraints": "FK -> users(id) NOT NULL",
        },
        {
            "column": "product_id",
            "type": "INTEGER",
            "constraints": "FK -> products(id) NOT NULL",
        },
        {"column": "quantity", "type": "INTEGER", "constraints": "NOT NULL"},
        {"column": "order_date", "type": "DATE", "constraints": "NOT NULL"},
        {
            "column": "status",
            "type": "VARCHAR(20)",
            "constraints": "CHECK (status IN ...)",
        },
    ],
    "reviews": [
        {"column": "id", "type": "INTEGER", "constraints": "PRIMARY KEY AUTOINCREMENT"},
        {
            "column": "product_id",
            "type": "INTEGER",
            "constraints": "FK -> products(id) NOT NULL",
        },
        {
            "column": "user_id",
            "type": "INTEGER",
            "constraints": "FK -> users(id) NOT NULL",
        },
        {
            "column": "rating",
            "type": "INTEGER",
            "constraints": "CHECK (rating BETWEEN 1 AND 5) NOT NULL",
        },
        {"column": "comment", "type": "TEXT", "constraints": "NULL"},
        {"column": "review_date", "type": "DATE", "constraints": "NOT NULL"},
    ],
}

RELATIONSHIPS: List[str] = [
    "users -> orders (One -> Many)",
    "users -> reviews (One -> Many)",
    "departments -> employees (One -> Many)",
    "employees -> employees (Manager -> Subordinates)",
    "categories -> products (One -> Many)",
    "suppliers -> products (One -> Many)",
    "products -> orders (One -> Many)",
    "products -> reviews (One -> Many)",
]
