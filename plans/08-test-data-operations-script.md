# Plan 08: Automated Data Operations Test Script

## Objective
Create a comprehensive Django management command that tests all CRUD operations across the system, verifies database changes, and reports results.

## Scope
Test all major models and their operations:
- Raw Materials (Create, Read, Update, Delete)
- Daily Consumption (Create, Read, Delete)
- Product Types (Create, Read, Update, Delete)
- Daily Production (Create, Read, Delete)
- Customers (Create, Read, Update, Delete)
- Purchase Orders (Create, Read, Update, Status Change, Delete)
- Purchase Order Items (Create, Read, Delete)
- Purchase Order Updates (Create, Read, Delete)

## Implementation

### 1. Create Management Command
**New File:** `core/management/commands/test_data_operations.py`

Structure:
```python
from django.core.management.base import BaseCommand
from django.utils import timezone
from core.models import (
    RawMaterial, DailyConsumption, ProductType,
    DailyProduction, Customer, PurchaseOrder,
    PurchaseOrderItem, PurchaseOrderUpdate
)

class Command(BaseCommand):
    help = 'Test all data CRUD operations'

    def handle(self, *args, **options):
        # Run all tests
        # Report results
```

### 2. Test Structure

Each model test should follow this pattern:

```
TEST: RawMaterial Operations
  ├── CREATE: Add new raw material
  ├── READ: Retrieve by ID
  ├── READ: List all materials
  ├── UPDATE: Modify material details
  ├── READ: Verify update
  ├── DELETE: Remove material
  ├── READ: Verify deletion
  └── RESULT: ✅ PASS or ❌ FAIL
```

### 3. Test Scenarios

#### Raw Materials
- Create material with all fields
- Verify fields were saved correctly
- Update material name/unit
- Verify update reflected in database
- Delete and verify deletion
- Test filtering by category

#### Daily Consumption
- Create consumption record with material FK
- Verify relationship intact
- Multiple records for same material
- Delete and verify cascade behavior
- Test date filtering

#### Product Types
- Create product type
- Verify creation
- Update description
- Delete product type
- Test that deleting doesn't break dependent productions

#### Daily Production
- Create production record
- Link to product type
- Add contents description
- Verify all fields
- Test quantity tracking
- Delete and verify

#### Customers
- Create customer with contact info
- Verify creation
- Update contact information
- Delete customer
- Verify related orders handled correctly

#### Purchase Orders (Complex)
- Create order with customer FK
- Create associated order items
- Verify relationship integrity
- Add items with quantities
- Test status changes (pending → in_progress → completed)
- Add delivery updates/notes
- Test overall_progress calculation
- Delete order and verify cascade

#### Purchase Order Items
- Create item with order + product FKs
- Update quantities (ordered vs fulfilled)
- Verify fulfillment tracking
- Delete item
- Verify order still exists

#### Purchase Order Updates
- Create update record for order
- Add delivery note and quantity
- Verify timestamp
- Delete update
- Verify order still exists

### 4. Test Data Fixtures

Create realistic test data:
- Raw materials: Chicken Breast, Ground Beef, Vegetables, Oil, Packaging
- Product types: Food Pack, Platter, Bilao
- Customers: ABC Restaurant, XYZ Catering, Local Business
- Orders with various statuses

### 5. Assertion Checks

For each operation, verify:

**CREATE:**
- Object created in database
- ID/UUID assigned
- All fields have correct values
- Timestamps set correctly
- Foreign keys resolved

**READ:**
- Can retrieve by primary key
- Can filter and search
- Related objects accessible
- No N+1 query issues

**UPDATE:**
- Changes persisted to database
- Modified timestamp updated
- Related objects unaffected
- Partial updates work

**DELETE:**
- Record removed from database
- No orphaned foreign keys
- Cascade behavior correct
- Soft delete not used (hard delete)

### 6. Output Format

Report should show:

```
════════════════════════════════════════════════════════
  KITCHEN MANAGEMENT SYSTEM - DATA OPERATIONS TEST
════════════════════════════════════════════════════════

TEST SUITE STARTED: 2024-01-15 14:30:00

1. RAW MATERIALS TESTS
   ├─ CREATE raw material ............................ ✅ PASS
   ├─ READ raw material by ID ....................... ✅ PASS
   ├─ UPDATE raw material ........................... ✅ PASS
   ├─ DELETE raw material ........................... ✅ PASS
   └─ Raw Materials: 4/4 PASSED

2. DAILY CONSUMPTION TESTS
   ├─ CREATE consumption record ..................... ✅ PASS
   ├─ READ consumption with FK ...................... ✅ PASS
   ├─ DELETE consumption record ..................... ✅ PASS
   └─ Daily Consumption: 3/3 PASSED

... [similar for all modules]

════════════════════════════════════════════════════════
SUMMARY
════════════════════════════════════════════════════════
Total Tests: 35
Passed: 35 ✅
Failed: 0 ❌
Success Rate: 100%

Test Duration: 2.34 seconds
════════════════════════════════════════════════════════

All tests completed successfully!
```

### 7. Error Handling

For each test:
- Catch exceptions
- Report error details
- Continue to next test (don't abort)
- Log stack trace if --verbose flag used

### 8. Usage

```bash
# Run all tests
python manage.py test_data_operations

# Run with verbose output
python manage.py test_data_operations --verbose

# Run specific test
python manage.py test_data_operations --test raw_materials

# Populate database with sample data for testing/demo
python manage.py test_data_operations --populate

# Populate sample data and run tests
python manage.py test_data_operations --populate --run-tests

# Save results to file
python manage.py test_data_operations > test_results.txt

# Clear all sample data that was created
python manage.py test_data_operations --clear-samples
```

### 9. Sample Data Population Feature

The script includes a `--populate` flag that creates realistic sample data for demo/testing:

**Sample Data Created:**
- 5 Raw Materials (Chicken Breast, Ground Beef, Vegetables, Oil, Packaging)
- 3 Product Types (Food Pack, Platter, Bilao)
- 4 Customers (ABC Restaurant, XYZ Catering, Local Business, Event Venue)
- 2 Daily Consumption records
- 3 Daily Production records
- 3 Purchase Orders with various statuses (Pending, In Progress, Completed)
- Multiple Purchase Order Items
- 2 Purchase Order Updates/delivery notes

**Features:**
- All sample data is created with proper relationships
- Realistic dates and quantities
- Sample data can coexist with real data
- Easy to identify: All named with "SAMPLE_" or "TEST_" prefix
- Can be individually deleted from the UI
- Can be bulk cleared with `--clear-samples` flag

**Use Cases:**
- New users can explore system with sample data
- Demos and training environments
- Testing UI/UX without affecting production
- Load testing with realistic data sizes

### 10. Database Cleanup

Important: All test data created should be:
- Marked as test data (prefix: "SAMPLE_" or "TEST_")
- Optionally cleaned up after tests complete with `--clear-samples`
- Can be selectively deleted from UI
- Can coexist with production data

### 11. Data Validation Checks

Beyond CRUD operations, also test:

```
VALIDATIONS:
├─ Model constraints enforced
├─ Required fields validation
├─ Unique field constraints
├─ Foreign key constraints
├─ Choice field validation
├─ Date/datetime fields
├─ Numeric field constraints
├─ String length limits
└─ Custom validators
```

### 12. Integration Tests

Test workflows:
1. **Full Order Workflow**
   - Create customer
   - Create products
   - Create order with multiple items
   - Update order status
   - Add delivery updates
   - Complete order
   - Verify all state changes

2. **Consumption Workflow**
   - Create raw materials
   - Record consumption multiple times
   - Verify totals
   - Test date range filtering

3. **Production Workflow**
   - Create products
   - Record production multiple times
   - Test quantity aggregation

### 13. Performance Testing

Optionally include timing:
- Time each CRUD operation
- Report slow operations
- Flag operations taking > 100ms
- Useful for identifying N+1 queries

### 14. File Structure

```
core/
├── management/
│   ├── __init__.py
│   └── commands/
│       ├── __init__.py
│       └── test_data_operations.py
├── models.py
├── views.py
└── ...
```

### 15. Exit Codes

- `0` - All tests passed
- `1` - One or more tests failed
- `2` - Test execution error

Useful for CI/CD pipelines.

## Success Criteria

✅ Tests all 8 models with CRUD operations
✅ Verifies database changes after each operation
✅ Clear pass/fail reporting
✅ All tests pass without errors
✅ Runs without modifying production data
✅ Cleanup removes test data
✅ Can be run repeatedly
✅ Performance metrics (optional)
✅ Clear output format
✅ Exit code reflects test results
✅ Verbose mode available for debugging

## Usage Recommendations

Run this test:
- Before deploying to production
- After database migrations
- Periodically to verify data integrity
- In CI/CD pipeline
- After code changes to models/views
- To validate model relationships

## Future Enhancements

- Add to CI/CD pipeline (GitHub Actions, etc.)
- Send results to dashboard/monitoring
- Alert on failures
- Track historical test results
- Add load/stress testing
- Generate test report HTML
- Integration with pytest
