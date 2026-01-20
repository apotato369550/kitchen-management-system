# Cebu Best Value Trading - Kitchen Management System

Track raw materials, production output, and customer orders in one place. Fast data entry, mobile-friendly, minimal complexity.

## Quick Start

**What:** Track ingredients used, products made, and orders from customers.

**Requirements:** Python 3.12+, PostgreSQL database

**Setup (local development):**
```bash
git clone <repository-url>
cd kitchen-management-system
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Configure `.env` file (see Installation section), then:
```bash
python manage.py setup_auth
python manage.py migrate
python manage.py runserver
```

Visit `http://127.0.0.1:8000/` to access the system.

---

## Installation

### Local Development Setup

**1. Clone and set up environment**
```bash
git clone <repository-url>
cd kitchen-management-system
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**2. Create `.env` file in project root**

Add database credentials (PostgreSQL via Render or Supabase):
```
DATABASE_URL=postgresql://user:password@host:5432/dbname
SECRET_KEY=your-secret-key-here
DEBUG=True
```

**3. Initialize database and user system**
```bash
python manage.py setup_auth       # Creates Admin, Management, Viewer roles
python manage.py migrate          # Applies all database migrations
python manage.py createsuperuser  # Creates first admin account
```

**4. Run development server**
```bash
python manage.py runserver
```

Login at `http://127.0.0.1:8000/accounts/login/` with your superuser account.

### Database Configuration

Use PostgreSQL (Render or Supabase). Connection string format:
```
postgresql://username:password@host:port/database_name
```

For first deployment to Render, `build.sh` handles migrations and setup automatically.

---

## Core Workflows

### Raw Materials

**What:** Maintain a catalog of ingredients and packaging (meat, vegetables, oil, etc.).

**How to use:**
1. Go to **Materials** menu
2. Click **Add Material**, enter name, category, unit (kg, liters, pieces)
3. Click **Save**

Use materials when recording daily consumption. Export as Excel/PDF from the materials list.

---

### Daily Consumption Tracker

**What:** Record how much of each material was used today.

**How to use:**
1. Go to **Consumption** menu
2. Click **Record Usage**
3. Select material, enter quantity used, date
4. Check "Add Another" to log multiple entries without page reload
5. Click **Save**

View consumption history with date and category filters. Delete and re-create records if corrections needed (no edit option). Export as Excel/PDF.

---

### Product Types

**What:** Define what you sell (food packs, platters, individual dishes, etc.).

**How to use:**
1. Go to **Products** menu
2. Click **Add Product**, enter name and optional description
3. Click **Save**

Use products when recording production and creating customer orders.

---

### Daily Production Tracker

**What:** Record how many of each product you made today.

**How to use:**
1. Go to **Production** menu
2. Click **Record Production**
3. Select product type, enter quantity made, date
4. Optionally add contents description (ingredient notes)
5. Check "Add Another" for fast sequential entry
6. Click **Save**

Records group by date in history view. Delete and re-create if corrections needed. Export as Excel/PDF.

---

### Customers

**What:** Maintain list of who you sell to.

**How to use:**
1. Go to **Customers** menu
2. Click **Add Customer**, enter name and optional contact info
3. Click **Save**

View all orders from a customer by clicking their name. Edit or delete customer info anytime. Deleting a customer also removes all their orders.

---

### Purchase Orders

**What:** Create and track customer orders with partial delivery tracking.

**How to use:**

**Create an order:**
1. Go to **Orders** menu, click **Create Order**
2. Select customer
3. Add items: select product type and quantity ordered
4. Click "Add More" to add additional products
5. Click **Create**

**Track fulfillment:**
1. From order detail page, click **Log Delivery Update**
2. Enter delivery note (e.g., "First batch delivered")
3. Optionally enter quantity delivered
4. Click **Save**

**Change order status:**
1. From order detail page, click **Change Status**
2. Select new status (pending, in progress, completed, cancelled)
3. Click **Update**

**Understand order progress:**
- Each order shows overall fulfillment % (how much delivered vs. ordered)
- Progress = (total items fulfilled / total items ordered) × 100
- Full delivery: all items at or above ordered quantity

---

## Key Concepts

**Staggered Fulfillment:** Orders don't need full delivery at once. Record partial deliveries over multiple days. Each update logs a delivery event with date and quantity.

**Order Progress %:** Shows fulfillment status. 50% = half of ordered items delivered. 100% = all items delivered (can exceed 100% if over-delivered).

**Data Export:** From any module list (Materials, Consumption, Products, Production, Customers, Orders), click **Export to Excel** or **Export to PDF** to download formatted reports with timestamps and summaries.

**Separate Tracking:** Raw materials and production are tracked independently. No automatic links between ingredient usage and product output. Track both manually as needed.

**Records Can't Be Edited:** For consumption and production, delete the record and re-create it if a mistake is made. For raw materials, products, and customers, edit directly.

---

## Troubleshooting

**"I can't see the Orders menu"**
- Check your login role. You need Admin or Management role. Ask admin to create your account.

**"I made a mistake in a consumption record"**
- Delete the record (click trash icon) and create a new one with correct data.

**"I can't delete a product"**
- The product is used in active orders. Check all orders for that product first.

**"My order isn't showing updated progress"**
- Log a delivery update first, then manually update fulfillment quantities from order detail page if needed.

**"Where's my exported file?"**
- Check your browser downloads folder. Files named like: `materials_excel_2025-01-20_14-30-45.xlsx`

**Database connection fails on startup**
- Verify `.env` has correct `DATABASE_URL`
- Confirm PostgreSQL host is reachable
- Check port 5432 is accessible from your machine

---

## For Admins

### User Management

**Access:** Go to **Admin** menu (visible if you're superuser), click **Users**

**Create user:**
1. Click **Create User**
2. Enter username, first/last name, email
3. Set password
4. Select role: Admin (full access) or Management (operations only)
5. Click **Create**

**Edit user:**
1. Find user in list, click their name
2. Update fields or change role
3. Click **Save**

**Delete user:**
1. Find user in list, click their name
2. Click **Delete**, confirm

**User profile:** Any user can go to **Profile** to change their own password.

### User Roles Explained

| Role | Can Do | Used For |
|------|--------|----------|
| Admin | Create users, manage all operations | Kitchen manager or owner |
| Management | Record consumption, production, orders, customers | Kitchen staff |
| Viewer | Reserved for future read-only access | (Not yet implemented) |

### First-Time Setup

On Render deployment:
1. `build.sh` automatically runs `python manage.py setup_auth`
2. This creates the three role groups (Admin, Management, Viewer)
3. A superuser is created with credentials from environment variables
4. Database migrations apply automatically

For local development, manually run:
```bash
python manage.py setup_auth
python manage.py migrate
python manage.py createsuperuser
```

---

## Common Tasks

**Log raw material usage:** Consumption → Record Usage → Select material, quantity, date → Add Another if multiple → Save

**Record what you produced:** Production → Record Production → Select product, quantity, date → Add Another if multiple → Save

**Create customer order:** Orders → Create Order → Select customer → Add items (product + quantity) → Create

**Track order delivery:** Orders → [Select order] → Log Delivery Update → Add delivery note → Save

**Export data for reporting:** [Any module list] → Export to Excel (or PDF) → Download file

**Check a customer's history:** Customers → [Click customer name] → View all their orders

**View system overview:** Dashboard (home page) shows counts of all records

---

## Tech Stack

- **Language:** Python 3.12+
- **Framework:** Django 6.0
- **Database:** PostgreSQL
- **Frontend:** Tailwind CSS (dark mode enabled)
- **Export:** Excel (openpyxl), PDF (ReportLab)
- **Deployment:** Render (Render PostgreSQL or Supabase for local dev)

---

## Deployment to Render

The system is configured for one-command deployment to Render.

**Prerequisites:**
- GitHub repository with code pushed to `main` branch
- Render account linked to GitHub
- PostgreSQL database created in Render

**Process:**
1. Push code to GitHub `main` branch
2. Render automatically detects changes and deploys
3. `build.sh` handles setup (migrations, user groups, static files)
4. Environment variables (ADMIN_USERNAME, ADMIN_PASSWORD, etc.) configured in Render dashboard
5. System available at Render-provided domain

**First Deploy Only:** Superuser created with `ADMIN_USERNAME` and `ADMIN_PASSWORD` from environment.

---

## Database Schema

All models use UUID for unique IDs.

- **Customer:** Contact information, linked to orders
- **RawMaterial:** Ingredients/packaging catalog (name, category, unit)
- **DailyConsumption:** Dated records of material usage
- **ProductType:** Sellable products (name, optional description)
- **DailyProduction:** Dated records of product output
- **PurchaseOrder:** Customer orders, status tracked (pending, in progress, completed, cancelled)
- **PurchaseOrderItem:** Line items in orders (product, quantity ordered, quantity fulfilled)
- **PurchaseOrderUpdate:** Delivery event log (notes, quantities, dates)

---

## Testing & Sample Data

### Create sample data
```bash
python manage.py test_data_operations --populate
```

Creates 5 materials, 3 products, 4 customers, 2 production records, 2 orders. All prefixed with `SAMPLE_` for easy identification.

### Clear sample data
```bash
python manage.py test_data_operations --clear-samples
```

### Run CRUD tests
```bash
python manage.py test_data_operations
```

Tests create, read, update, delete operations across all modules.

---

## Support

This is a private project. For questions or issues, contact the project owner.

---

## License

Proprietary - All rights reserved
