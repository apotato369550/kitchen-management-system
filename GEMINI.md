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
    *   **Admin:** Full access (User management + Operations).
    *   **Management:** Operations only (Raw materials, Production, Orders).

## Tech Stack

*   **Language:** Python 3.12+
*   **Framework:** Django 6.0
*   **Frontend:** Tailwind CSS (served via Django templates)
*   **Database:** PostgreSQL (Supabase via connection pooler)
*   **Hosting:** Vercel (Primary), Render (Alternative build script present)
*   **Dependencies:** `django-axes`, `gunicorn`, `whitenoise`, `dj-database-url`, `reportlab`, `openpyxl`.

## Project Structure

```text
/home/jay/Desktop/Coding Stuff/kitchen-management-system/
├── accounts/                      # Authentication app (User management, Login/Logout)
├── core/                          # Main business logic
│   ├── models.py                  # Core database models (Customer, RawMaterial, etc.)
│   ├── views.py                   # View controllers (CRUD + Exports)
│   ├── forms.py                   # Django forms
│   ├── services/                  # Business logic services (e.g., export.py)
│   └── templates/core/            # UI Templates
├── kitchen_management_system/     # Project configuration (settings.py, urls.py)
├── plans/                         # Implementation documentation & roadmap
├── manage.py                      # Django CLI entry point
├── .env                           # Environment variables (Sensitive!)
└── requirements.txt               # Python dependencies
```

## Key Workflows

### 1. Development Server
```bash
source venv/bin/activate
python manage.py runserver
```

### 2. Database Migrations
**Important:** The project uses Supabase. Ensure `.env` is configured correctly before migrating.
```bash
python manage.py makemigrations
python manage.py migrate
```

### 3. Testing
**General Tests:**
```bash
python manage.py test
```

**Data Operations Test Script:**
A custom management command is available for comprehensive testing and sample data generation.
```bash
# Run CRUD tests
python manage.py test_data_operations

# Populate sample data
python manage.py test_data_operations --populate

# Clear sample data
python manage.py test_data_operations --clear-samples
```

## Database Schema (Key Models)

All models use UUIDs for primary keys.

*   **`Customer`**: Basic contact info.
*   **`RawMaterial`**: Ingredients/Packaging (Name, Category, Unit).
*   **`DailyConsumption`**: Tracks usage of raw materials per day.
*   **`ProductType`**: Definition of sellable items (Food packs, Platters).
*   **`DailyProduction`**: Tracks output of products per day.
*   **`PurchaseOrder`**: Orders linked to a Customer. Supports staggered fulfillment.
*   **`PurchaseOrderItem`**: Line items in an order.
*   **`PurchaseOrderUpdate`**: Log of updates/partial deliveries for an order.

## Deployment

*   **Platform:** Vercel
*   **Config:** `vercel.json` (Assumed standard Vercel Django setup)
*   **Static Files:** Handled by `whitenoise` in production; `collectstatic` required during build.

## Current Status (v0.3.0)

*   **Completed:**
    *   Auth System (Admin/Management).
    *   Database Schema & Migrations.
    *   CRUD Views for all models.
    *   Dark Mode UI.
    *   Data Export (Excel & PDF).
    *   Sample Data Generator.
*   **Pending/In-Progress:**
    *   Refinement of UI for specific trackers (Plan 04 & 05).
    *   Scheduled automatic exports.

## Interaction Guidelines for Gemini

*   **Context Awareness:** Always check `models.py` and `views.py` in `core/` before suggesting changes to business logic.
*   **Style:** Match the existing Tailwind CSS usage in templates.
*   **Safety:** Never output the contents of `.env`.
*   **Conciseness:** Be brief. The user values efficiency and clarity.
