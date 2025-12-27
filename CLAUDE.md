# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Kitchen management and purchase order system for a food business. Three main features:

1. **Authentication System** - Secure, admin-controlled user management. No public signup - only admins can create accounts.

2. **Raw Materials + Production Tracker** - Daily recording of raw materials consumed (meat, vegetables, oil, packaging with various measurements) and production output (food packs, platters/bilao, contents). No conversion relationship between inputs and outputs.

3. **Purchase Order Tracker** - Create, update, monitor purchase orders associated with customers. Orders can be fulfilled in full or staggered with update history (comment-style).

## Tech Stack

- **Backend**: Django 6.0
- **Frontend**: Tailwind CSS with light theme
- **Database**: PostgreSQL (Render)
- **Authentication**: Django's built-in auth system
- **Hosting**: Vercel
- **Python**: 3.12+

## Database Connection

Uses Render PostgreSQL:
- Host: Configured via `SUPABASE_HOST` environment variable
- Port: `5432`
- User: Configured via `SUPABASE_USER` environment variable
- Password: Stored in `.env` file as `SUPABASE_PROJECT_PASSWORD`

## User Roles

### Admin
- Full system access
- Can create, edit, and delete user accounts
- Can manage all data (raw materials, production, purchase orders)

### Management (Owner & Secretary)
- Can manage daily operations
- Cannot create or manage user accounts
- Access to all operational features

## Design Philosophy

**SLEEK AND SIMPLE.** Follow the owner's vision exactly:
- No feature creep
- No unsolicited additions
- No overcomplicated UI
- Fast data entry priority
- Mobile-friendly (kitchen environment)
- Clean, minimalist design

## Project Structure

```
kitchen-management-system/
├── core/                          # Main app: models, views, templates, services
│   ├── migrations/                # Database migrations
│   ├── management/commands/       # Management commands
│   │   └── test_data_operations.py  # CRUD testing & sample data
│   ├── services/                  # Utility services
│   │   └── export.py              # PDF/Excel export functions
│   ├── templates/core/            # HTML templates
│   ├── static/core/               # CSS, JS files
│   ├── models.py                  # 8 models (Customer, RawMaterial, etc.)
│   ├── views.py                   # View functions (40+ views including exports)
│   ├── forms.py                   # Form classes
│   ├── urls.py                    # URL routing (45+ endpoints)
│   └── admin.py                   # Admin panel config
├── accounts/                      # Auth app with user management
├── kitchen_management_system/     # Django project settings
│   ├── settings.py                # Main settings file
│   ├── urls.py                    # Root URL config
│   └── wsgi.py                    # WSGI entry point
├── plans/                         # Implementation plans
│   ├── 01-database-schema.md
│   ├── 02-django-init.md
│   ├── 03-authentication-system.md
│   ├── 04-raw-materials-production-tracker.md
│   └── 05-purchase-order-tracker.md
├── .env                           # Environment variables (not in git)
├── .gitignore
├── manage.py
├── requirements.txt
├── README.md                      # Developer instructions
├── CHANGELOG.md                   # Change history
└── INSTRUCTIONS.md                # Original project requirements
```

## Database Models (Implemented)

All models use UUID primary keys for database compatibility:

1. **Customer** - name, contact_info, created_at
2. **RawMaterial** - name, category (enum), unit
3. **DailyConsumption** - date, raw_material (FK), quantity, created_at
4. **ProductType** - name, description
5. **DailyProduction** - date, product_type (FK), quantity, contents_description, created_at
6. **PurchaseOrder** - customer (FK), status (enum), created_at, updated_at
7. **PurchaseOrderItem** - purchase_order (FK), product_type (FK), quantity_ordered, quantity_fulfilled
8. **PurchaseOrderUpdate** - purchase_order (FK), note, quantity_delivered, created_at

## Current Implementation Status

### ✅ Completed (Version 0.3.1)
- Django project initialized with Django 6.0
- Database models (8 models) created and migrated to Render PostgreSQL
- Authentication system with user roles (Admin, Management) - Plan 03
- Full CRUD operations for all models
- Professional light theme UI with Tailwind CSS (upgraded from dark mode)
- Responsive design with touch-friendly buttons
- 40+ view functions with proper authentication checks
- 45+ URL endpoints with organized routing
- **Data Export System** (Plan 07):
  - Excel export for all 6 modules
  - PDF export for all 6 modules with professional formatting
  - Export service module with reusable functions
  - Timestamped filenames
- **Test Data Operations** (Plan 08):
  - CRUD testing command for all modules
  - Sample data population with `--populate` flag
  - Clear sample data with `--clear-samples` flag
  - Test-specific modules with `--test` flag
- **UI/UX Redesign** (Plan 09):
  - Light theme with enhanced typography (17px base, bolder labels)
  - Larger logo with prominent "CBVT Kitchen Management System" branding
  - User management with responsive cards/tables
  - All list view actions converted to styled buttons
  - Empty state warnings on create forms
  - Recent additions sidebars (top 10 records) on create forms
  - Production history grouped by date with visual headers
  - "Add Another Item" button properly styled
- Site rebranding from "KitchenHub" to "Cebu Best Value Trading"
- Tutorial feature removed (Plan 06) for cleaner codebase
- Dashboard with quick access cards
- Login/logout with throttling
- User management interface with role assignment
- Comprehensive documentation in README.md, CHANGELOG.md, CLAUDE.md, GEMINI.md

### 🚧 In Progress
- None currently

### 📋 Planned (see plans/ directory)
- CSV export format support
- Scheduled automatic exports
- Additional reporting features
- Advanced analytics dashboard

## Development Guidelines

### Code Style
- Follow Django best practices
- Use class-based views where appropriate
- Keep views simple and focused
- Use Django forms for all user input
- Implement proper validation

### Security
- All views require authentication (except login)
- Use CSRF protection on all forms
- Validate user permissions (admin vs management)
- Sanitize user input
- Use parameterized queries (Django ORM handles this)

### UI/UX
- Mobile-first responsive design
- Large, touch-friendly buttons
- Clear error messages
- Fast page loads
- Minimal clicks to complete tasks

### Testing
- Write tests for critical business logic
- Test all forms and validation
- Test permission enforcement
- Test edge cases (empty data, invalid input)

## Key Implementation Notes

1. **No Input-Output Conversion**: Raw materials and production are tracked separately with no automated conversion logic.

2. **Staggered Fulfillment**: Purchase orders support partial deliveries tracked via PurchaseOrderUpdate model.

3. **Admin-Only User Creation**: No signup page. Admins create accounts through user management panel.

4. **Mobile-Friendly**: Kitchen environment requires touch-friendly interface.

5. **Simple Over Clever**: Prefer straightforward implementations over clever abstractions.

## Common Tasks

### Run Development Server
```bash
source venv/bin/activate  # or .\venv\Scripts\activate on Windows
python manage.py runserver
```

### Create/Apply Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### Access Django Admin
```bash
python manage.py createsuperuser  # First time only
# Then visit http://127.0.0.1:8000/admin/
```

### Run Tests
```bash
python manage.py test
```

## Environment Variables

Required in `.env` file:
- `SUPABASE_PROJECT_PASSWORD` - Render database password
- `SUPABASE_HOST` - Render PostgreSQL host
- `SUPABASE_PORT` - Render PostgreSQL port (5432)
- `SUPABASE_USER` - Render database username
- `SECRET_KEY` - Django secret key (generate new for production)
- `DEBUG` - True for development, False for production

## Git Workflow

- Keep commits atomic and well-described
- Reference plan files in commit messages when implementing features
- Never commit `.env` file or secrets
- Update CHANGELOG.md with significant changes

## Questions or Clarifications

If requirements are unclear:
1. Check INSTRUCTIONS.md for original requirements
2. Check relevant plan file in plans/ directory
3. Ask the project owner (user) for clarification
4. Keep it simple - avoid assumptions
