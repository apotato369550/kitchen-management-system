# Data Testing & Sample Data Operations

This guide explains how to use the `test_data_operations` management command to test your database, create sample data, and verify data integrity.

## Overview

The `test_data_operations` command provides four key functions:
- **CRUD Testing (`--test`)**: Verify Create, Read, Update, and Delete operations for each data model.
- **Sample Data Population (`--populate`)**: Populate the database with realistic demo data for testing and training.
- **Data Cleanup (`--clear-samples`)**: Remove all sample data with a single command, leaving your real data untouched.
- **Verbose Output (`--verbose`)**: Show detailed information for each test.

## Quick Start

### Test Everything
Runs a full suite of CRUD tests across all modules.
```bash
python manage.py test_data_operations
```

### Create Sample Data
Populates the database with a set of realistic, interconnected sample records.
```bash
python manage.py test_data_operations --populate
```

### See Detailed Test Output
Runs all tests and shows step-by-step results.
```bash
python manage.py test_data_operations --verbose
```

### Remove All Sample Data
Deletes all records that were created by the `--populate` command.
```bash
python manage.py test_data_operations --clear-samples
```

## Complete Command Reference

### `test_data_operations`
Runs the complete suite of CRUD tests for all 8 models. Exits with code 0 on success and 1 on failure.
```bash
python manage.py test_data_operations
```

### `--populate`
Creates sample data. If run alone, it only populates the data. It can be combined with `--test` to run tests after populating.
```bash
python manage.py test_data_operations --populate
```

### `--clear-samples`
Removes all data where the `name` or description field starts with `SAMPLE_`. This is safe to run on a database with real data.
```bash
python manage.py test_data_operations --clear-samples
```

### `--test <module_name>`
Tests a specific module instead of all of them.
```bash
python manage.py test_data_operations --test raw_materials
```
**Available modules:**
- `raw_materials`
- `consumption`
- `product_types`
- `production`
- `customers`
- `purchase_orders`

### `--verbose`
Shows detailed pass/fail information for every single test operation (CREATE, READ, UPDATE, DELETE).
```bash
python manage.py test_data_operations --verbose
```

## Sample Data Details

When you run `--populate`, the following records are created. All are prefixed with `SAMPLE_` for easy identification.

#### Raw Materials
1.  `SAMPLE_Chicken Breast` (Meat, kg)
2.  `SAMPLE_Ground Beef` (Meat, kg)
3.  `SAMPLE_Vegetables Mix` (Vegetables, kg)
4.  `SAMPLE_Cooking Oil` (Oil, liters)
5.  `SAMPLE_Packaging Material` (Miscellaneous, pieces)

#### Product Types
1.  `SAMPLE_Food Pack`
2.  `SAMPLE_Platter`
3.  `SAMPLE_Bilao`

#### Customers
1.  `SAMPLE_ABC Restaurant` (555-0001)
2.  `SAMPLE_XYZ Catering` (555-0002)
3.  `SAMPLE_Local Business` (555-0003)
4.  `SAMPLE_Event Venue` (555-0004)

#### Daily Records & Orders
- **Daily Consumption**: 3 records using the first few sample materials.
- **Daily Production**: 3 records, one for each sample product type.
- **Purchase Orders**: 2 orders created for the first two customers, each containing two order items and an initial update log.

## Understanding Test Output

### Standard Output (Success)
```
$ python manage.py test_data_operations

============================================================
  CEBU BEST VALUE TRADING - DATA OPERATIONS TEST
============================================================

📅 TEST SUITE STARTED: 2025-12-25 14:00:00

RAW MATERIALS TESTS
   └─ Raw Materials: 4/4 PASSED

CONSUMPTION TESTS
   └─ Consumption: 3/3 PASSED

... (other modules) ...

============================================================
SUMMARY
============================================================

Total Tests: 24
Passed: 24 ✅
Failed: 0 ❌
Success Rate: 100.0%

Test Duration: 1.88 seconds

All tests completed successfully! 🎉
```

### Verbose Output (with a Failure)
```
$ python manage.py test_data_operations --verbose

...
PURCHASE ORDERS TESTS
   ├─ CREATE purchase order ✅ PASS
   ├─ CREATE order item ✅ PASS
   ├─ CREATE order update ✅ PASS
   ├─ UPDATE order status ❌ FAIL
      Error: 'status' must be one of the choices.
   ├─ DELETE order (cascade) ✅ PASS
   └─ Purchase Orders: 4/5 PASSED

============================================================
SUMMARY
============================================================

Total Tests: 24
Passed: 23 ✅
Failed: 1 ❌
...
1 test(s) failed!
```

## Exit Codes

The command returns specific exit codes, which is useful for CI/CD pipelines.
-   **`0`**: Success. All tests passed.
-   **`1`**: Test Failure. One or more tests failed.
-   **`2`**: Command Error. An issue occurred like a database connection error (not a test failure).

You can use this in a script:
```bash
python manage.py test_data_operations
if [ $? -eq 0 ]; then
  echo "✅ Data integrity tests passed."
else
  echo "❌ Data integrity tests failed. Check logs."
  exit 1
fi
```

## Common Workflows

### 1. Initial Setup & Verification
After cloning the repo and setting up your `.env` file:
```bash
# 1. Apply database migrations
python manage.py migrate

# 2. Run all data integrity tests
python manage.py test_data_operations
```

### 2. Demo or Training Setup
To show the system to someone, you can quickly populate it with data.
```bash
# 1. Populate with sample data
python manage.py test_data_operations --populate

# 2. Start the server and log in
python manage.py runserver

# 3. When finished, clean up the database
python manage.py test_data_operations --clear-samples
```

### 3. Verifying Changes
After you modify a model in `core/models.py`:
```bash
# 1. Create a new migration for your changes
python manage.py makemigrations

# 2. Apply the migration
python manage.py migrate

# 3. Run the full test suite to ensure your changes didn't break anything
python manage.py test_data_operations --verbose
```