# GEMINI.md

This file provides context and instructions for Gemini when working on the "Cebu Best Value Trading" Kitchen Management System.

## Project Overview

**Name:** Cebu Best Value Trading Kitchen Management System
**Purpose:** A specialized kitchen management and purchase order tracking system for a food business.
**Core Philosophy:** **SLEEK AND SIMPLE.** The user's vision is paramount. Avoid feature creep, over-engineering, or unsolicited "AI ideas." Focus on fast data entry, mobile-friendliness, and a clean, minimalist design.

## Core Mandates

1.  **Strict Adherence to Vision:** Do not suggest new features unless explicitly asked. Implement exactly what is requested.
2.  **No Correlation (Yet):** Raw material inputs and production outputs are tracked separately. Do not attempt to build automated conversion logic between them.
3.  **Authentication:** No public signup. Admins create accounts.
4.  **User Roles:**
    *   **Admin:** Full access (User management + Operations). Can be a superuser.
    *   **Management:** Operations only (Raw materials, Production, Orders).
    *   **Viewer:** (Future use) Intended for read-only access. The group is created but not currently used in any views.

## Tech Stack

*   **Language:** Python 3.12+
*   **Framework:** Django 6.0
*   **Frontend:** Tailwind CSS
*   **Database:** PostgreSQL (primary deployment via Render, can connect to Supabase for local dev)
*   **Hosting:** **Render**
*   **Dependencies:** `django-axes` (security), `gunicorn` (server), `whitenoise` (static files), `dj-database-url` (db connection), `reportlab` (PDF), `openpyxl` (Excel).

## Project Structure

```text
/
├── accounts/                  # User management, login/logout, roles
├── core/                      # Main business logic (models, views, forms)
│   ├── services/              # Business logic services (e.g., export.py)
│   └── management/commands/   # Custom Django commands (test_data, create_superuser)
├── kitchen_management_system/ # Django project configuration (settings.py, urls.py)
├── plans/                     # Implementation documentation & roadmap
├── build.sh                   # Deployment build script for Render
├── render.yaml                # Infrastructure-as-code for Render
├── manage.py                  # Django CLI entry point
├── .env                       # Environment variables (local development)
└── requirements.txt           # Python dependencies
```

## Key Workflows & Commands

### 1. Development Server (Local)
Requires a `.env` file configured for a database (e.g., Supabase).
```bash
# Set up the database with initial groups and a default admin
python manage.py setup_auth

# Run the server
python manage.py runserver
```

### 2. Database Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 3. Testing & Sample Data
A custom management command is available for comprehensive testing.
```bash
# Run all CRUD tests
python manage.py test_data_operations

# Populate the database with realistic sample data
python manage.py test_data_operations --populate

# Clear all sample data
python manage.py test_data_operations --clear-samples
```

## Database Schema (`core/models.py`)

All models use UUIDs for primary keys.

*   **`Customer`**: Basic contact info.
*   **`RawMaterial`**: Ingredients/Packaging (Name, Category, Unit).
*   **`DailyConsumption`**: Tracks usage of raw materials per day.
*   **`ProductType`**: Definition of sellable items (Food packs, Platters).
*   **`DailyProduction`**: Tracks output of products per day.
*   **`PurchaseOrder`**: Orders linked to a Customer. Supports staggered fulfillment.
*   **`PurchaseOrderItem`**: Line items in an order.
*   **`PurchaseOrderUpdate`**: Log of updates/partial deliveries for an order.

## Deployment (Render)

*   **Platform:** Render
*   **Configuration:** `render.yaml` defines the web service and database.
*   **Build Process:** `build.sh` script installs dependencies, collects static files, runs migrations, and creates user groups and a superuser.
*   **Continuous Deployment:** Pushing to the `main` branch on GitHub automatically triggers a new deployment on Render.
*   **Superuser Creation:** On first deploy, a superuser is created using credentials from environment variables set in `render.yaml` (`ADMIN_USERNAME`, `ADMIN_PASSWORD`, etc.).

## Current Status (v0.3.0)

*   **Completed:**
    *   Auth System (Admin/Management roles).
    *   Database Schema & Migrations for all 8 models.
    *   Full CRUD views for all models.
    *   Dark Mode UI with Tailwind CSS.
    *   Data Export to Excel & PDF for all modules.
    *   Robust `test_data_operations` command for testing and sample data.
    *   Deployment configuration for **Render**.
*   **Pending/In-Progress:**
    *   Refinement of UI for specific trackers (Plan 04 & 05).

## Interaction Guidelines for Gemini

*   **Context Awareness:** Always check `core/models.py` and `core/views.py` before suggesting changes to business logic.
*   **Style:** Match the existing Tailwind CSS usage and Django patterns.
*   **Deployment:** Be aware that the project is deployed on **Render**. Changes to `render.yaml` or `build.sh` will affect deployment.
*   **Safety:** Never output the contents of `.env`.
*   **Conciseness:** Be brief. The user values efficiency and clarity.