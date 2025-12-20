"""
Management command to test all CRUD operations in the kitchen management system.
Can also populate sample data for demos/testing.

Usage:
    python manage.py test_data_operations              # Run all tests
    python manage.py test_data_operations --populate   # Create sample data
    python manage.py test_data_operations --clear-samples  # Remove sample data
"""
import sys
from datetime import datetime, timedelta
from django.core.management.base import BaseCommand
from django.utils import timezone

from core.models import (
    RawMaterial, DailyConsumption, ProductType,
    DailyProduction, Customer, PurchaseOrder,
    PurchaseOrderItem, PurchaseOrderUpdate
)


class Command(BaseCommand):
    help = 'Test all CRUD operations and verify database changes'

    def add_arguments(self, parser):
        parser.add_argument(
            '--populate',
            action='store_true',
            help='Populate database with sample data'
        )
        parser.add_argument(
            '--clear-samples',
            action='store_true',
            help='Clear sample data from database'
        )
        parser.add_argument(
            '--test',
            type=str,
            help='Run specific test (raw_materials, consumption, etc)'
        )
        parser.add_argument(
            '--verbose',
            action='store_true',
            help='Show detailed output'
        )

    def handle(self, *args, **options):
        if options['clear_samples']:
            self.clear_sample_data()
            return

        if options['populate']:
            self.populate_sample_data()
            if not (options.get('test') or options.get('verbose')):
                self.stdout.write(
                    self.style.SUCCESS('✅ Sample data created successfully!')
                )
            return

        # Run tests
        self.run_tests(options)

    def print_header(self, text):
        """Print formatted header"""
        self.stdout.write('\n' + '=' * 60)
        self.stdout.write(self.style.WARNING(f'  {text}'))
        self.stdout.write('=' * 60)

    def print_test(self, name, status, error=None):
        """Print test result"""
        status_symbol = '✅ PASS' if status else '❌ FAIL'
        self.stdout.write(f'   ├─ {name} {status_symbol}')
        if error and not status:
            self.stdout.write(self.style.ERROR(f'      Error: {error}'))

    def run_tests(self, options):
        """Run all CRUD tests"""
        self.print_header('CEBU BEST VALUE TRADING - DATA OPERATIONS TEST')
        self.stdout.write(f'\n📅 TEST SUITE STARTED: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}\n')

        start_time = datetime.now()
        test_counts = {}
        total_passed = 0
        total_failed = 0

        # Run specific test if requested
        if options.get('test'):
            test_name = options['test']
            passed, failed = self.test_module(test_name)
            total_passed += passed
            total_failed += failed
        else:
            # Run all tests
            modules = [
                'raw_materials', 'consumption', 'product_types',
                'production', 'customers', 'purchase_orders'
            ]
            for module in modules:
                passed, failed = self.test_module(module)
                total_passed += passed
                total_failed += failed
                test_counts[module] = (passed, failed)

        # Summary
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()

        self.print_header('SUMMARY')
        self.stdout.write(f'\nTotal Tests: {total_passed + total_failed}')
        self.stdout.write(self.style.SUCCESS(f'Passed: {total_passed} ✅'))
        self.stdout.write(self.style.ERROR(f'Failed: {total_failed} ❌'))

        success_rate = (total_passed / (total_passed + total_failed) * 100) if (total_passed + total_failed) > 0 else 0
        self.stdout.write(f'Success Rate: {success_rate:.1f}%')
        self.stdout.write(f'\nTest Duration: {duration:.2f} seconds\n')

        if total_failed == 0:
            self.stdout.write(self.style.SUCCESS('All tests completed successfully! 🎉\n'))
            sys.exit(0)
        else:
            self.stdout.write(self.style.ERROR(f'{total_failed} test(s) failed!\n'))
            sys.exit(1)

    def test_module(self, module_name):
        """Test a specific module"""
        tests = {
            'raw_materials': self.test_raw_materials,
            'consumption': self.test_consumption,
            'product_types': self.test_product_types,
            'production': self.test_production,
            'customers': self.test_customers,
            'purchase_orders': self.test_purchase_orders,
        }

        if module_name not in tests:
            self.stdout.write(self.style.ERROR(f'❌ Unknown module: {module_name}'))
            return 0, 1

        self.stdout.write(f'\n{module_name.upper().replace("_", " ")} TESTS')
        return tests[module_name]()

    def test_raw_materials(self):
        """Test RawMaterial CRUD operations"""
        passed = 0
        failed = 0

        try:
            # CREATE
            material = RawMaterial.objects.create(
                name='TEST_Chicken Breast',
                category='meat',
                unit='grams'
            )
            assert material.pk is not None
            self.print_test('CREATE raw material', True)
            passed += 1
        except Exception as e:
            self.print_test('CREATE raw material', False, str(e))
            failed += 1
            return passed, failed

        try:
            # READ
            retrieved = RawMaterial.objects.get(pk=material.pk)
            assert retrieved.name == 'TEST_Chicken Breast'
            self.print_test('READ raw material by ID', True)
            passed += 1
        except Exception as e:
            self.print_test('READ raw material by ID', False, str(e))
            failed += 1

        try:
            # LIST
            materials = RawMaterial.objects.filter(name__startswith='TEST_')
            assert len(materials) > 0
            self.print_test('LIST raw materials', True)
            passed += 1
        except Exception as e:
            self.print_test('LIST raw materials', False, str(e))
            failed += 1

        try:
            # UPDATE
            material.unit = 'kg'
            material.save()
            updated = RawMaterial.objects.get(pk=material.pk)
            assert updated.unit == 'kg'
            self.print_test('UPDATE raw material', True)
            passed += 1
        except Exception as e:
            self.print_test('UPDATE raw material', False, str(e))
            failed += 1

        try:
            # DELETE
            material.delete()
            with self.assertRaises(RawMaterial.DoesNotExist):
                RawMaterial.objects.get(pk=material.pk)
            self.print_test('DELETE raw material', True)
            passed += 1
        except RawMaterial.DoesNotExist:
            self.print_test('DELETE raw material', True)
            passed += 1
        except Exception as e:
            self.print_test('DELETE raw material', False, str(e))
            failed += 1

        self.stdout.write(f'   └─ Raw Materials: {passed}/{passed + failed} PASSED\n')
        return passed, failed

    def test_consumption(self):
        """Test DailyConsumption CRUD operations"""
        passed = 0
        failed = 0

        # Create material first
        material = RawMaterial.objects.create(
            name='TEST_Vegetables',
            category='vegetables',
            unit='kg'
        )

        try:
            # CREATE
            consumption = DailyConsumption.objects.create(
                raw_material=material,
                quantity=5.5,
                date=timezone.now().date()
            )
            assert consumption.pk is not None
            self.print_test('CREATE consumption record', True)
            passed += 1
        except Exception as e:
            self.print_test('CREATE consumption record', False, str(e))
            failed += 1
            return passed, failed

        try:
            # READ with FK
            retrieved = DailyConsumption.objects.select_related('raw_material').get(pk=consumption.pk)
            assert retrieved.raw_material.pk == material.pk
            self.print_test('READ consumption with FK', True)
            passed += 1
        except Exception as e:
            self.print_test('READ consumption with FK', False, str(e))
            failed += 1

        try:
            # DELETE
            consumption.delete()
            material.delete()
            self.print_test('DELETE consumption record', True)
            passed += 1
        except Exception as e:
            self.print_test('DELETE consumption record', False, str(e))
            failed += 1

        self.stdout.write(f'   └─ Consumption: {passed}/{passed + failed} PASSED\n')
        return passed, failed

    def test_product_types(self):
        """Test ProductType CRUD operations"""
        passed = 0
        failed = 0

        try:
            # CREATE
            product = ProductType.objects.create(
                name='TEST_Food Pack',
                description='Sample food pack for testing'
            )
            assert product.pk is not None
            self.print_test('CREATE product type', True)
            passed += 1
        except Exception as e:
            self.print_test('CREATE product type', False, str(e))
            failed += 1
            return passed, failed

        try:
            # READ
            retrieved = ProductType.objects.get(pk=product.pk)
            assert retrieved.name == 'TEST_Food Pack'
            self.print_test('READ product type', True)
            passed += 1
        except Exception as e:
            self.print_test('READ product type', False, str(e))
            failed += 1

        try:
            # UPDATE
            product.description = 'Updated description'
            product.save()
            updated = ProductType.objects.get(pk=product.pk)
            assert updated.description == 'Updated description'
            self.print_test('UPDATE product type', True)
            passed += 1
        except Exception as e:
            self.print_test('UPDATE product type', False, str(e))
            failed += 1

        try:
            # DELETE
            product.delete()
            self.print_test('DELETE product type', True)
            passed += 1
        except Exception as e:
            self.print_test('DELETE product type', False, str(e))
            failed += 1

        self.stdout.write(f'   └─ Product Types: {passed}/{passed + failed} PASSED\n')
        return passed, failed

    def test_production(self):
        """Test DailyProduction CRUD operations"""
        passed = 0
        failed = 0

        # Create product type first
        product = ProductType.objects.create(
            name='TEST_Platter',
            description='Test platter'
        )

        try:
            # CREATE
            production = DailyProduction.objects.create(
                product_type=product,
                quantity=10,
                contents_description='Test contents',
                date=timezone.now().date()
            )
            assert production.pk is not None
            self.print_test('CREATE production record', True)
            passed += 1
        except Exception as e:
            self.print_test('CREATE production record', False, str(e))
            failed += 1
            return passed, failed

        try:
            # READ
            retrieved = DailyProduction.objects.select_related('product_type').get(pk=production.pk)
            assert retrieved.product_type.pk == product.pk
            self.print_test('READ production record', True)
            passed += 1
        except Exception as e:
            self.print_test('READ production record', False, str(e))
            failed += 1

        try:
            # DELETE
            production.delete()
            product.delete()
            self.print_test('DELETE production record', True)
            passed += 1
        except Exception as e:
            self.print_test('DELETE production record', False, str(e))
            failed += 1

        self.stdout.write(f'   └─ Production: {passed}/{passed + failed} PASSED\n')
        return passed, failed

    def test_customers(self):
        """Test Customer CRUD operations"""
        passed = 0
        failed = 0

        try:
            # CREATE
            customer = Customer.objects.create(
                name='TEST_ABC Restaurant',
                contact_info='555-1234'
            )
            assert customer.pk is not None
            self.print_test('CREATE customer', True)
            passed += 1
        except Exception as e:
            self.print_test('CREATE customer', False, str(e))
            failed += 1
            return passed, failed

        try:
            # READ
            retrieved = Customer.objects.get(pk=customer.pk)
            assert retrieved.name == 'TEST_ABC Restaurant'
            self.print_test('READ customer', True)
            passed += 1
        except Exception as e:
            self.print_test('READ customer', False, str(e))
            failed += 1

        try:
            # UPDATE
            customer.contact_info = '555-5678'
            customer.save()
            updated = Customer.objects.get(pk=customer.pk)
            assert updated.contact_info == '555-5678'
            self.print_test('UPDATE customer', True)
            passed += 1
        except Exception as e:
            self.print_test('UPDATE customer', False, str(e))
            failed += 1

        try:
            # DELETE
            customer.delete()
            self.print_test('DELETE customer', True)
            passed += 1
        except Exception as e:
            self.print_test('DELETE customer', False, str(e))
            failed += 1

        self.stdout.write(f'   └─ Customers: {passed}/{passed + failed} PASSED\n')
        return passed, failed

    def test_purchase_orders(self):
        """Test PurchaseOrder complex CRUD operations"""
        passed = 0
        failed = 0

        # Create customer and product
        customer = Customer.objects.create(
            name='TEST_Customer',
            contact_info='555-1234'
        )
        product = ProductType.objects.create(
            name='TEST_Product',
            description='Test product'
        )

        try:
            # CREATE order
            order = PurchaseOrder.objects.create(
                customer=customer,
                status='pending'
            )
            assert order.pk is not None
            self.print_test('CREATE purchase order', True)
            passed += 1
        except Exception as e:
            self.print_test('CREATE purchase order', False, str(e))
            failed += 1
            return passed, failed

        try:
            # CREATE order items
            item = PurchaseOrderItem.objects.create(
                purchase_order=order,
                product_type=product,
                quantity_ordered=5,
                quantity_fulfilled=0
            )
            assert item.pk is not None
            self.print_test('CREATE order item', True)
            passed += 1
        except Exception as e:
            self.print_test('CREATE order item', False, str(e))
            failed += 1

        try:
            # CREATE order update
            update = PurchaseOrderUpdate.objects.create(
                purchase_order=order,
                note='TEST: Partial delivery',
                quantity_delivered=2
            )
            assert update.pk is not None
            self.print_test('CREATE order update', True)
            passed += 1
        except Exception as e:
            self.print_test('CREATE order update', False, str(e))
            failed += 1

        try:
            # UPDATE status
            order.status = 'in_progress'
            order.save()
            updated = PurchaseOrder.objects.get(pk=order.pk)
            assert updated.status == 'in_progress'
            self.print_test('UPDATE order status', True)
            passed += 1
        except Exception as e:
            self.print_test('UPDATE order status', False, str(e))
            failed += 1

        try:
            # DELETE order (cascade)
            order.delete()
            self.print_test('DELETE order (cascade)', True)
            passed += 1
        except Exception as e:
            self.print_test('DELETE order (cascade)', False, str(e))
            failed += 1

        # Cleanup
        customer.delete()
        product.delete()

        self.stdout.write(f'   └─ Purchase Orders: {passed}/{passed + failed} PASSED\n')
        return passed, failed

    def populate_sample_data(self):
        """Populate database with realistic sample data"""
        self.stdout.write('📊 Populating sample data...')

        # Clear existing sample data
        RawMaterial.objects.filter(name__startswith='SAMPLE_').delete()
        ProductType.objects.filter(name__startswith='SAMPLE_').delete()
        Customer.objects.filter(name__startswith='SAMPLE_').delete()

        # Create raw materials
        materials = []
        material_data = [
            ('Chicken Breast', 'meat', 'kg'),
            ('Ground Beef', 'meat', 'kg'),
            ('Vegetables Mix', 'vegetables', 'kg'),
            ('Cooking Oil', 'oil', 'liters'),
            ('Packaging Material', 'miscellaneous', 'pieces'),
        ]
        for name, category, unit in material_data:
            m = RawMaterial.objects.create(
                name=f'SAMPLE_{name}',
                category=category,
                unit=unit
            )
            materials.append(m)

        # Create consumption records
        for material in materials[:3]:
            DailyConsumption.objects.create(
                raw_material=material,
                quantity=2.5,
                date=timezone.now().date()
            )

        # Create product types
        products = []
        product_data = [
            ('Food Pack', 'Standard meal pack'),
            ('Platter', 'Large serving platter'),
            ('Bilao', 'Traditional bilao serving'),
        ]
        for name, description in product_data:
            p = ProductType.objects.create(
                name=f'SAMPLE_{name}',
                description=description
            )
            products.append(p)

        # Create production records
        for product in products:
            DailyProduction.objects.create(
                product_type=product,
                quantity=15,
                contents_description='SAMPLE_Food',
                date=timezone.now().date()
            )

        # Create customers
        customers = []
        customer_data = [
            ('ABC Restaurant', '555-0001'),
            ('XYZ Catering', '555-0002'),
            ('Local Business', '555-0003'),
            ('Event Venue', '555-0004'),
        ]
        for name, contact in customer_data:
            c = Customer.objects.create(
                name=f'SAMPLE_{name}',
                contact_info=contact
            )
            customers.append(c)

        # Create purchase orders
        for customer in customers[:2]:
            order = PurchaseOrder.objects.create(
                customer=customer,
                status='pending'
            )
            for product in products[:2]:
                PurchaseOrderItem.objects.create(
                    purchase_order=order,
                    product_type=product,
                    quantity_ordered=5,
                    quantity_fulfilled=0
                )

            # Add delivery update
            PurchaseOrderUpdate.objects.create(
                purchase_order=order,
                note='SAMPLE_Initial order created',
                quantity_delivered=0
            )

        self.stdout.write(self.style.SUCCESS('✅ Sample data created!'))
        self.stdout.write(f'   • 5 Raw Materials')
        self.stdout.write(f'   • 3 Product Types')
        self.stdout.write(f'   • 4 Customers')
        self.stdout.write(f'   • 2 Production Records')
        self.stdout.write(f'   • 2 Purchase Orders')

    def clear_sample_data(self):
        """Remove all sample data from database"""
        self.stdout.write('🗑️  Clearing sample data...')

        count = 0
        count += RawMaterial.objects.filter(name__startswith='SAMPLE_').delete()[0]
        count += ProductType.objects.filter(name__startswith='SAMPLE_').delete()[0]
        count += DailyProduction.objects.filter(product_type__name__startswith='SAMPLE_').delete()[0]
        count += DailyConsumption.objects.filter(raw_material__name__startswith='SAMPLE_').delete()[0]
        count += PurchaseOrder.objects.filter(customer__name__startswith='SAMPLE_').delete()[0]
        count += Customer.objects.filter(name__startswith='SAMPLE_').delete()[0]

        self.stdout.write(self.style.SUCCESS(f'✅ Cleared {count} records!'))

    def assertRaises(self, exception):
        """Helper for testing exceptions"""
        class ContextManager:
            def __enter__(self):
                return self

            def __exit__(self, exc_type, exc_val, exc_tb):
                if exc_type is None:
                    raise AssertionError(f'Expected {exception} but nothing was raised')
                if not issubclass(exc_type, exception):
                    return False
                return True

        return ContextManager()
