# Data Testing & Sample Data Operations

This guide explains how to use the `test_data_operations` management command to test your database, create sample data, and verify data integrity.

## Overview

The `test_data_operations` command provides:
- **CRUD Testing** - Verify Create, Read, Update, Delete operations work correctly
- **Sample Data** - Populate realistic demo data for testing and training
- **Data Cleanup** - Remove all sample data with a single command
- **Module Testing** - Test specific modules in isolation

## Quick Start

### Test Everything
```bash
python manage.py test_data_operations
```

### Create Sample Data
```bash
python manage.py test_data_operations --populate
```

### Remove Sample Data
```bash
python manage.py test_data_operations --clear-samples
```

## Complete Command Reference

### Run All CRUD Tests
Tests all 6 modules (raw materials, consumption, products, production, customers, purchase orders):
```bash
python manage.py test_data_operations
```

**Output:**
- ✅ Pass/fail for each test
- Summary with total passed/failed counts
- Execution time
- Exit code (0 = success, 1 = failure)

### Run Tests with Verbose Output
Shows detailed information about each test as it runs:
```bash
python manage.py test_data_operations --verbose
```

### Test Specific Module
Test only one module instead of all:
```bash
python manage.py test_data_operations --test raw_materials
```

**Available modules:**
- `raw_materials` - RawMaterial CRUD operations
- `consumption` - DailyConsumption CRUD operations
- `product_types` - ProductType CRUD operations
- `production` - DailyProduction CRUD operations
- `customers` - Customer CRUD operations
- `purchase_orders` - PurchaseOrder and related CRUD operations

### Populate Sample Data
Create realistic demo data with proper relationships:
```bash
python manage.py test_data_operations --populate
```

**Creates:**
- 5 Raw Materials (Chicken Breast, Ground Beef, Vegetables, Oil, Packaging)
- 3 Product Types (Food Pack, Platter, Bilao)
- 4 Customers (ABC Restaurant, XYZ Catering, Local Business, Event Venue)
- 2 Daily Consumption records
- 2 Daily Production records
- 2 Purchase Orders with delivery updates

**All sample data is marked with `SAMPLE_` prefix** for easy identification and deletion from the UI.

### Clear Sample Data
Remove all sample data from the database:
```bash
python manage.py test_data_operations --clear-samples
```

**Only removes records with `SAMPLE_` prefix** - your real data is safe.

## Common Workflows

### Workflow 1: Create & Test Sample Data
```bash
# 1. Populate sample data
python manage.py test_data_operations --populate

# 2. Run tests with verbose output
python manage.py test_data_operations --verbose

# 3. Review sample data in the UI by logging in
# Visit http://127.0.0.1:8000/

# 4. Delete sample data when done
python manage.py test_data_operations --clear-samples
```

### Workflow 2: Test Individual Modules
```bash
# Test raw materials only
python manage.py test_data_operations --test raw_materials

# Test consumption only
python manage.py test_data_operations --test consumption

# Test purchase orders (most complex)
python manage.py test_data_operations --test purchase_orders
```

### Workflow 3: Demo/Training Setup
```bash
# 1. Populate realistic sample data
python manage.py test_data_operations --populate

# 2. Start development server
python manage.py runserver

# 3. Login and explore with sample data
# Raw materials are in: Raw Materials > Library
# Production is in: Production > History
# Orders are in: Sales > Orders

# 4. Delete when training is done
python manage.py test_data_operations --clear-samples
```

### Workflow 4: Verify Data Integrity After Changes
```bash
# After modifying models or making code changes
python manage.py test_data_operations --verbose

# If all tests pass: ✅ System is healthy
# If tests fail: ❌ Review the errors and fix the issues
```

## What Gets Tested

### Raw Materials
- ✅ Create raw material
- ✅ Read by ID
- ✅ List all materials
- ✅ Update fields
- ✅ Delete material

### Daily Consumption
- ✅ Create consumption record
- ✅ Read with foreign key relationship
- ✅ Delete with cascade handling

### Product Types
- ✅ Create product
- ✅ Read by ID
- ✅ Update description
- ✅ Delete product

### Daily Production
- ✅ Create production record
- ✅ Read with foreign key
- ✅ Delete with cascade

### Customers
- ✅ Create customer
- ✅ Read by ID
- ✅ Update contact info
- ✅ Delete customer

### Purchase Orders (Complex)
- ✅ Create purchase order
- ✅ Create order items
- ✅ Create order updates
- ✅ Update order status
- ✅ Delete with cascade handling

## Sample Data Details

When you run `--populate`, this is created:

### Raw Materials (SAMPLE_ prefix)
1. SAMPLE_Chicken Breast (Meat, kg)
2. SAMPLE_Ground Beef (Meat, kg)
3. SAMPLE_Vegetables Mix (Vegetables, kg)
4. SAMPLE_Cooking Oil (Oil, liters)
5. SAMPLE_Packaging Material (Miscellaneous, pieces)

### Product Types (SAMPLE_ prefix)
1. SAMPLE_Food Pack - Standard meal pack
2. SAMPLE_Platter - Large serving platter
3. SAMPLE_Bilao - Traditional bilao serving

### Customers (SAMPLE_ prefix)
1. SAMPLE_ABC Restaurant (555-0001)
2. SAMPLE_XYZ Catering (555-0002)
3. SAMPLE_Local Business (555-0003)
4. SAMPLE_Event Venue (555-0004)

### Production Records (SAMPLE_ prefix)
- 2 production records for sample products
- Quantity: 15 units each
- Today's date

### Purchase Orders (SAMPLE_ prefix)
- 2 orders for first 2 customers
- 2 items per order (first 2 products)
- Status: Pending
- Includes delivery update records

## Understanding Test Output

### Successful Test Run
```
============================================================
  CEBU BEST VALUE TRADING - DATA OPERATIONS TEST
============================================================

📅 TEST SUITE STARTED: 2025-12-21 10:30:00

RAW MATERIALS TESTS
   ├─ CREATE raw material ✅ PASS
   ├─ READ raw material by ID ✅ PASS
   ├─ UPDATE raw material ✅ PASS
   ├─ DELETE raw material ✅ PASS
   └─ Raw Materials: 4/4 PASSED

...

============================================================
SUMMARY
============================================================

Total Tests: 24
Passed: 24 ✅
Failed: 0 ❌
Success Rate: 100.0%

Test Duration: 2.34 seconds

All tests completed successfully! 🎉
```

### Failed Test Run
```
...
   ├─ UPDATE consumption record ❌ FAIL
      Error: Field 'quantity' must be numeric
...

Failed: 1 ❌

Test Duration: 1.45 seconds

1 test(s) failed!
```

## Troubleshooting

### Database Connection Error
```
Error: Could not connect to database
```
**Solution:** Verify `.env` file has correct Supabase credentials and the database is running.

### Sample Data Already Exists
```
python manage.py test_data_operations --clear-samples
```
Then run populate again.

### Tests Fail After Code Changes
This indicates a bug in your code. Review the error message carefully:
- Check the model definition
- Verify database migrations are applied
- Check for missing foreign key relationships

### Permission Denied Error
Ensure you're in the project root directory:
```bash
cd /path/to/kitchen-management-system
python manage.py test_data_operations
```

## Tips & Best Practices

### For Development
1. Use `--populate` to create test data
2. Run `--test raw_materials` to verify basic CRUD works
3. Delete with `--clear-samples` before committing code

### For Demos
1. Run `--populate` to load sample data
2. Login and show features with real-looking data
3. Clean up with `--clear-samples` when done

### For CI/CD
```bash
# Run tests and fail if any fail
python manage.py test_data_operations
if [ $? -ne 0 ]; then
  echo "Data integrity tests failed!"
  exit 1
fi
```

### For Deployment Verification
Before deploying to production:
```bash
# Run full test suite
python manage.py test_data_operations --verbose

# All tests must pass ✅
```

## Sample Data Deletion

All sample data uses the `SAMPLE_` prefix, making it easy to delete:

### Via Django Admin
1. Login to `/admin/`
2. Find any record with `SAMPLE_` in the name
3. Delete directly

### Via Management Command
```bash
python manage.py test_data_operations --clear-samples
```

### Via UI
Any user can delete sample records from the list views just like regular data.

## Exit Codes

The command returns different exit codes for CI/CD integration:
- **0** - All tests passed ✅
- **1** - One or more tests failed ❌
- **2** - Command execution error

Use in scripts:
```bash
python manage.py test_data_operations
if [ $? -eq 0 ]; then
  echo "✅ All tests passed"
else
  echo "❌ Tests failed"
fi
```

## Examples

### Example 1: Quick System Health Check
```bash
$ python manage.py test_data_operations

✅ All tests completed successfully!
Success Rate: 100%
```

### Example 2: Detailed Testing with Verbose
```bash
$ python manage.py test_data_operations --verbose

RAW MATERIALS TESTS
   ├─ CREATE raw material ✅ PASS
   ├─ READ raw material by ID ✅ PASS
   ...
✅ All tests completed successfully!
```

### Example 3: Demo Data Setup
```bash
$ python manage.py test_data_operations --populate
✅ Sample data created!
   • 5 Raw Materials
   • 3 Product Types
   • 4 Customers
   • 2 Production Records
   • 2 Purchase Orders
```

### Example 4: Test Single Module
```bash
$ python manage.py test_data_operations --test customers

CUSTOMERS TESTS
   ├─ CREATE customer ✅ PASS
   ├─ READ customer ✅ PASS
   ├─ UPDATE customer ✅ PASS
   ├─ DELETE customer ✅ PASS
   └─ Customers: 4/4 PASSED
```

## Need Help?

For more details, see:
- `README.md` - General project setup
- `CHANGELOG.md` - Version 0.3.0 for testing feature details
- `plans/08-test-data-operations-script.md` - Technical implementation details
