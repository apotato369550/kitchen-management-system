# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned
- Authentication system implementation
- Raw materials + production tracker UI
- Purchase order tracker UI
- Tailwind CSS integration
- User management interface

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
