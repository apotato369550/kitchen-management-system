# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- **Comprehensive Documentation Suite (Scalpel Phase 1)**
  - `ARCHITECTURE.md` (2,200+ lines): Deterministic, greppable system architecture with all 40+ endpoints, 8 data models, 10 critical gotchas, export patterns, permission matrix, and grep index
  - **README.md** (364 lines): Rewritten user-centric documentation for end users (kitchen staff, managers, admins) with quick start, installation, 6 core workflows, troubleshooting, and admin guide
  - **CLAUDE.md** (302 lines): Enhanced with 5 new agent-facing sections—data model constraints, permission & role model, view architecture, critical gaps, and working guidelines with file:line references

---

## [0.3.1] - 2025-12-27

### Changed
- **UI/UX Redesign** (Plan 09)
  - Upgraded from dark mode to light theme for better readability and professional appearance
  - Enhanced typography: 17px base font size with bolder form labels for better visibility
  - Larger logo with "CBVT Kitchen Management System" prominent branding in navigation
  - User management interface redesigned with responsive cards and tables
  - All list view action links converted to styled buttons for consistency and touch-friendliness
  - Empty state warnings on create forms (consumption, production, orders) with clear icons and instructions
  - Recent additions sidebars on all create forms showing top 10 records for quick reference
  - Production history now groups records by date with visual day headers for easier scanning
  - "Add Another Item" button properly styled and positioned
  - Improved form spacing and visual hierarchy throughout application

- **Database Documentation Correction**
  - Updated documentation to reflect Render PostgreSQL (corrected from Supabase references)
  - Environment variable naming clarified for Render database configuration

## [0.3.0] - 2025-12-20

### Added
- **Data Export Functionality** (Plan 07)
  - Excel export for all 6 data modules (Raw Materials, Consumption, Products, Production, Customers, Orders)
  - PDF export for all 6 data modules with professional formatting
  - Export service module (`core/services/export.py`) with reusable export functions
  - Timestamped export filenames for automatic organization
  - Excel: Formatted headers, auto-column widths, summary statistics
  - PDF: Headers with company branding, metadata, summary sections, professional table formatting
  - 12 new export views with proper authentication checks

- **Test Data Operations Management Command** (Plan 08)
  - Comprehensive CRUD testing across all 8 models
  - `--populate` flag to create realistic sample data for demos/testing
  - `--clear-samples` flag to remove all sample data
  - `--test` flag to test specific modules
  - `--verbose` flag for detailed test output
  - Sample data marked with `SAMPLE_` prefix for easy identification
  - Creates 5 raw materials, 3 products, 4 customers, 2 orders in sample mode
  - Test results with pass/fail reporting and execution timing

- **Site Rebranding**
  - Renamed site from "KitchenHub" to "Cebu Best Value Trading - Kitchen Management System"
  - Updated page titles, navigation branding, and welcome messages
  - Company name displayed prominently in login page and navigation bar

- **Tutorial Feature Removal** (Plan 06)
  - Removed Driver.js tutorial library and all related code
  - Removed tutorial database fields and migrations
  - Removed tutorial views, URLs, static files, and template references
  - Cleaner codebase with fewer external dependencies

### Changed
- Enhanced `requirements.txt` with export dependencies:
  - `reportlab>=4.0.0` for PDF generation
  - `openpyxl>=3.10.0` for Excel file generation
- Updated `core/urls.py` with 12 new export endpoints
- Enhanced `core/views.py` with 12 export view functions
- Updated `README.md` with export and testing documentation
- Improved documentation for export features and testing capabilities

### Removed
- Interactive tutorial feature (Driver.js implementation)
- Tutorial static files (`tutorial.js`, `tutorial-overrides.css`)
- Tutorial database model and views
- Tutorial references from templates

### Planned
- Raw materials + production tracker UI
- Purchase order tracker UI
- CSV export format support
- Scheduled automatic exports

## [0.2.0] - 2025-12-15

### Added
- Complete authentication system with Django's built-in auth
- `accounts` app with user management functionality
- User groups: Admin and Management
- Login/logout views with custom authentication form
- User management interface (admin-only):
  - User list view with status and role indicators
  - User creation form with role selection
  - User edit form with role management
  - User deletion with confirmation
- Permission decorators:
  - `@admin_required` - Restricts views to Admin group
  - `@management_or_admin_required` - Restricts to Management or Admin
- Login throttling with django-axes (5 failed attempts, 1-hour lockout)
- Dashboard view with authentication requirement
- Management command `setup_auth` to create groups and default admin
- Tailwind CSS integration via CDN
- Professional UI templates:
  - Base template with navigation and messages
  - Login page with clean form design
  - User management pages with tables and forms
  - Dashboard with feature cards
- Password validation (minimum 10 characters)
- Security settings configured for production (HTTPS, secure cookies)
- Authentication backends configuration

### Changed
- Updated `core/views.py` to use `@login_required` decorator
- Changed root URL from "Hello World" to protected dashboard
- Updated `requirements.txt` to include `django-axes>=6.0.0`
- Enhanced settings.py with:
  - LOGIN_URL, LOGIN_REDIRECT_URL, LOGOUT_REDIRECT_URL
  - AUTHENTICATION_BACKENDS with django-axes
  - Stronger password validation (10 character minimum)
  - Production security settings (commented for development)

### Security
- Implemented login rate limiting (django-axes)
- Added CSRF protection on all forms
- Password complexity requirements enforced
- Session security configured
- Production HTTPS settings prepared

## [0.1.0] - 2025-12-15

### Added
- Initial Django 6.0 project setup
- Virtual environment configuration
- Database models for complete system:
  - Customer model with name and contact information
  - RawMaterial model with categories (meat, vegetables, oil, miscellaneous)
  - DailyConsumption model for tracking raw material usage
  - ProductType model for product definitions
  - DailyProduction model for tracking production output
  - PurchaseOrder model with status tracking
  - PurchaseOrderItem model for order line items
  - PurchaseOrderUpdate model for comment-style update history
- Supabase PostgreSQL database connection via connection pooler (IPv4)
- Environment variable configuration (.env file)
- Core app with basic structure
- Initial database migration (0001_initial)
- Hello World test view at root URL
- Requirements.txt with dependencies:
  - django
  - psycopg2-binary
  - python-dotenv
- Implementation plans:
  - 03-authentication-system.md
  - 04-raw-materials-production-tracker.md
  - 05-purchase-order-tracker.md
- Project documentation:
  - README.md with development instructions
  - CLAUDE.md (root) with project context and structure
  - CLAUDE.md files in subdirectories (core, kitchen_management_system, plans)
  - CHANGELOG.md (this file)
  - INSTRUCTIONS.md (original requirements)

### Changed
- Updated settings.py to load environment variables via python-dotenv
- Modified database configuration to use connection pooler instead of direct connection
- Added 'core' app to INSTALLED_APPS
- Updated .env file with Supabase connection pooler credentials
- Modified plans/02-django-init.md to remove "stopped here" marker

### Fixed
- IPv6 connectivity issue by switching to Supabase connection pooler
- Database connection configuration for Supabase compatibility
- Added DEFAULT_AUTO_FIELD setting to avoid warnings

### Technical Details
- Database Host: aws-1-ap-south-1.pooler.supabase.com
- Database Port: 6543
- Database User: postgres.obfyvlyycxvtmbfnwbuw
- All models use UUID primary keys for Supabase compatibility
- Database tables use custom names (e.g., 'customers', 'raw_materials')

### Migration History
- Initial migration applied successfully to Supabase database
- All Django built-in app migrations applied (admin, auth, contenttypes, sessions)
- Core app migrations applied (8 custom models)

## [0.0.1] - 2025-12-14

### Added
- Repository initialization
- Git repository setup
- Initial planning documents:
  - 01-database-schema.md
  - 02-django-init.md
- requirements.txt skeleton
- Project directory structure

---

## Changelog Guidelines

### Types of Changes
- **Added** - New features or functionality
- **Changed** - Changes to existing functionality
- **Deprecated** - Soon-to-be removed features
- **Removed** - Removed features
- **Fixed** - Bug fixes
- **Security** - Security improvements

### When to Update
Update this file when:
- Adding new features
- Modifying existing features
- Fixing bugs
- Making configuration changes
- Updating dependencies
- Completing implementation milestones

### Version Format
- Major version (X.0.0) - Breaking changes
- Minor version (0.X.0) - New features, backward compatible
- Patch version (0.0.X) - Bug fixes, backward compatible

### Date Format
Use ISO 8601 format: YYYY-MM-DD
