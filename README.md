# Cebu Best Value Trading - Kitchen Management System

A Django-based kitchen management and purchase order tracking system for food businesses.

## Features

- **Authentication System**: Secure admin-controlled user management
- **Raw Materials Tracker**: Daily recording of consumed raw materials (meat, vegetables, oil, packaging)
- **Production Tracker**: Daily tracking of production output (food packs, platters, bilao)
- **Purchase Order Management**: Create and manage customer orders with staggered fulfillment tracking
- **Data Export**: Export all data to Excel and PDF formats for reporting and backup
- **Professional UI**: Light theme with enhanced typography, responsive cards/tables, and touch-friendly buttons for kitchen environment
- **Empty State Warnings**: Clear notifications on forms when prerequisite data doesn't exist
- **Recent Activity Sidebars**: Quick access to top 10 recently added records on create forms
- **Production History Grouping**: Records grouped by date with visual day headers for easier scanning

## Tech Stack

- **Backend**: Django 6.0
- **Frontend**: Tailwind CSS
- **Database**: PostgreSQL (Render)
- **Hosting**: Vercel
- **Python**: 3.12+

## Prerequisites

- Python 3.12 or higher
- PostgreSQL database (via Render or another PostgreSQL provider)
- Git

## Development Setup

### 1. Clone the Repository
```bash
git clone <repository-url>
cd kitchen-management-system
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Create a `.env` file in the root directory:
```env
# Render PostgreSQL Database Configuration
SUPABASE_PROJECT_PASSWORD=your_password_here
SUPABASE_HOST=your_render_postgres_host
SUPABASE_PORT=5432
SUPABASE_USER=your_db_user

# Django Secret Key (generate a new one for production)
SECRET_KEY=your_secret_key_here

# Debug (set to False in production)
DEBUG=True
```

**Important**: Never commit the `.env` file to version control.

### 5. Run Migrations
```bash
python manage.py migrate
```

### 6. Create Superuser (Admin Account)
```bash
python manage.py createsuperuser
```

### 7. Run Development Server
```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000/` to view the application.

## Project Structure

```
kitchen-management-system/
├── core/                          # Main application
│   ├── migrations/                # Database migrations
│   ├── templates/                 # HTML templates
│   ├── static/                    # Static files (CSS, JS)
│   ├── models.py                  # Database models
│   ├── views.py                   # View functions
│   ├── forms.py                   # Form classes
│   ├── urls.py                    # URL routing
│   └── admin.py                   # Admin configuration
├── accounts/                      # Authentication app (future)
├── kitchen_management_system/     # Project settings
│   ├── settings.py                # Django settings
│   ├── urls.py                    # Root URL configuration
│   └── wsgi.py                    # WSGI configuration
├── plans/                         # Implementation plans
├── .env                           # Environment variables (not in git)
├── manage.py                      # Django management script
└── requirements.txt               # Python dependencies
```

## Database Models

- **Customer**: Customer information and contact details
- **RawMaterial**: Raw materials library with categories and units
- **DailyConsumption**: Daily raw material consumption records
- **ProductType**: Product types (food packs, platters, etc.)
- **DailyProduction**: Daily production output records
- **PurchaseOrder**: Customer purchase orders with status tracking
- **PurchaseOrderItem**: Line items for each purchase order
- **PurchaseOrderUpdate**: Update history for orders (comment-style)

## User Roles

- **Admin**: Full system access, can create and manage users
- **Management**: Can manage daily operations (raw materials, production, orders)

## Development Workflow

### Making Database Changes
1. Modify models in `core/models.py`
2. Create migration: `python manage.py makemigrations`
3. Review migration file in `core/migrations/`
4. Apply migration: `python manage.py migrate`

### Running Tests
```bash
python manage.py test
```

### Creating a New App
```bash
python manage.py startapp app_name
```
Add the app to `INSTALLED_APPS` in `settings.py`.

### Accessing Django Admin
1. Ensure you've created a superuser (see step 6 above)
2. Visit `http://127.0.0.1:8000/admin/`
3. Login with superuser credentials

## Deployment

### Vercel Deployment
1. Install Vercel CLI: `npm i -g vercel`
2. Configure `vercel.json` (see deployment docs)
3. Set environment variables in Vercel dashboard
4. Deploy: `vercel --prod`

### Environment Variables for Production
Set these in your Vercel dashboard:
- `SUPABASE_PROJECT_PASSWORD` (Render database password)
- `SUPABASE_HOST` (Render PostgreSQL host)
- `SUPABASE_PORT` (Usually 5432 for Render)
- `SUPABASE_USER` (Render database user)
- `SECRET_KEY` (Strong, unique key for production)
- `DEBUG=False`

### Security Checklist for Production
- [ ] Set `DEBUG=False`
- [ ] Configure `ALLOWED_HOSTS`
- [ ] Use strong `SECRET_KEY`
- [ ] Enable HTTPS (Vercel does this automatically)
- [ ] Set secure cookie flags in settings
- [ ] Review CORS settings
- [ ] Set up proper logging

## Common Commands

```bash
# Start development server
python manage.py runserver

# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Open Django shell
python manage.py shell

# Collect static files (for production)
python manage.py collectstatic

# Run tests
python manage.py test

# Check for issues
python manage.py check
```

## Data Export

### Excel Export
Export any data module to Excel format:
- **Raw Materials**: `/raw-materials/export/excel/`
- **Consumption**: `/consumption/export/excel/`
- **Products**: `/product-types/export/excel/`
- **Production**: `/production/export/excel/`
- **Customers**: `/customers/export/excel/`
- **Orders**: `/orders/export/excel/`

### PDF Export
Export any data module to PDF format:
- **Raw Materials**: `/raw-materials/export/pdf/`
- **Consumption**: `/consumption/export/pdf/`
- **Products**: `/product-types/export/pdf/`
- **Production**: `/production/export/pdf/`
- **Customers**: `/customers/export/pdf/`
- **Orders**: `/orders/export/pdf/`

All exports include:
- Formatted headers with company branding
- Export timestamp
- Summary statistics
- Professional styling for print/sharing

## Testing & Sample Data

### Run Tests
Test all CRUD operations in the system:
```bash
python manage.py test_data_operations
```

### Populate Sample Data
Create realistic sample data for demos and testing:
```bash
python manage.py test_data_operations --populate
```

This creates:
- 5 raw materials with various categories
- 3 product types
- 4 sample customers
- 2 production records
- 2 purchase orders

All sample data is marked with `SAMPLE_` prefix for easy identification and deletion.

### Clear Sample Data
Remove all sample data from the database:
```bash
python manage.py test_data_operations --clear-samples
```

### Verbose Testing
Run tests with detailed output:
```bash
python manage.py test_data_operations --verbose
```

### Test Specific Module
Test a specific module's operations:
```bash
python manage.py test_data_operations --test raw_materials
```

Available modules: `raw_materials`, `consumption`, `product_types`, `production`, `customers`, `purchase_orders`

## Troubleshooting

### Database Connection Issues
- Verify `.env` file contains correct Render PostgreSQL credentials
- Check that Render PostgreSQL database is active and running
- Ensure port 5432 is accessible from your environment

### Migration Issues
- Delete `core/migrations/` except `__init__.py`
- Run `python manage.py makemigrations core`
- Run `python manage.py migrate`

### Static Files Not Loading
- Run `python manage.py collectstatic`
- Check `STATIC_URL` and `STATIC_ROOT` in settings

## Contributing

This is a private project. For questions or issues, contact the project owner.

## License

Proprietary - All rights reserved

## Contact

For support or questions, contact: [Your Email]
