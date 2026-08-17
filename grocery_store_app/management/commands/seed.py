from django.core.management.base import BaseCommand
from grocery_store_app.models import Category, Product, Store, StoreOpeningHours, PerStoreProduct
from datetime import time


class Command(BaseCommand):
    help = "Seed the database with sample categories, products, stores, and inventory"

    def add_arguments(self, parser):
        parser.add_argument(
            "--clear",
            action="store_true",
            help="Clear existing data before seeding",
        )

    def handle(self, *args, **options):
        if options["clear"]:
            self.stdout.write("Clearing existing data...")
            PerStoreProduct.objects.all().delete()
            Product.objects.all().delete()
            Category.objects.all().delete()
            StoreOpeningHours.objects.all().delete()
            Store.objects.all().delete()

        self._create_categories()
        self._create_stores()
        self._create_products()
        self._create_inventory()
        self.stdout.write(self.style.SUCCESS("Database seeded successfully."))

    def _create_categories(self):
        categories = ["Fruits", "Vegetables", "Dairy", "Meat", "Bakery", "Beverages", "Snacks", "Frozen"]
        for name in categories:
            Category.objects.get_or_create(name=name)
        self.stdout.write(f"  Created {len(categories)} categories")

    def _create_stores(self):
        stores_data = [
            {
                "name": "GSC Melbourne Central",
                "address": "211 La Trobe St, Melbourne VIC 3000",
                "postcode": "3000",
                "phone_number": "(03) 9654 1234",
                "hours": {
                    "monday_open": time(7, 0), "monday_close": time(21, 0),
                    "tuesday_open": time(7, 0), "tuesday_close": time(21, 0),
                    "wednesday_open": time(7, 0), "wednesday_close": time(21, 0),
                    "thursday_open": time(7, 0), "thursday_close": time(21, 0),
                    "friday_open": time(7, 0), "friday_close": time(21, 0),
                    "saturday_open": time(8, 0), "saturday_close": time(20, 0),
                    "sunday_open": time(9, 0), "sunday_close": time(18, 0),
                },
            },
            {
                "name": "GSC South Yarra",
                "address": "162 Toorak Rd, South Yarra VIC 3141",
                "postcode": "3141",
                "phone_number": "(03) 9826 5678",
                "hours": {
                    "monday_open": time(8, 0), "monday_close": time(20, 0),
                    "tuesday_open": time(8, 0), "tuesday_close": time(20, 0),
                    "wednesday_open": time(8, 0), "wednesday_close": time(20, 0),
                    "thursday_open": time(8, 0), "thursday_close": time(21, 0),
                    "friday_open": time(8, 0), "friday_close": time(21, 0),
                    "saturday_open": time(8, 0), "saturday_close": time(19, 0),
                    "sunday_open": time(9, 0), "sunday_close": time(17, 0),
                },
            },
            {
                "name": "GSC Carlton",
                "address": "305 Lygon St, Carlton VIC 3053",
                "postcode": "3053",
                "phone_number": "(03) 9347 9012",
                "hours": {
                    "monday_open": time(7, 30), "monday_close": time(20, 30),
                    "tuesday_open": time(7, 30), "tuesday_close": time(20, 30),
                    "wednesday_open": time(7, 30), "wednesday_close": time(20, 30),
                    "thursday_open": time(7, 30), "thursday_close": time(20, 30),
                    "friday_open": time(7, 30), "friday_close": time(21, 0),
                    "saturday_open": time(8, 0), "saturday_close": time(20, 0),
                    "sunday_open": time(9, 0), "sunday_close": time(17, 0),
                },
            },
        ]

        for store_data in stores_data:
            hours_data = store_data.pop("hours")
            store, created = Store.objects.get_or_create(
                name=store_data["name"],
                defaults=store_data,
            )
            if created:
                StoreOpeningHours.objects.get_or_create(store=store, defaults=hours_data)

        self.stdout.write(f"  Created {len(stores_data)} stores")

    def _create_products(self):
        products_data = [
            ("Bananas", 3.50, "Fruits", "https://images.unsplash.com/photo-1571771894821-ce9b6c11b08e?w=300"),
            ("Strawberries", 5.99, "Fruits", "https://images.unsplash.com/photo-1464965911861-746a04b4bca6?w=300"),
            ("Avocados", 2.50, "Fruits", "https://images.unsplash.com/photo-1523049673857-eb18f1d7b578?w=300"),
            ("Apples", 4.99, "Fruits", "https://images.unsplash.com/photo-1560806887-1e4cd0b6cbd6?w=300"),
            ("Oranges", 6.99, "Fruits", "https://images.unsplash.com/photo-1547514701-42782101795e?w=300"),
            ("Broccoli", 3.99, "Vegetables", "https://images.unsplash.com/photo-1459411552884-841db9b3cc2a?w=300"),
            ("Carrots", 2.49, "Vegetables", "https://images.unsplash.com/photo-1598170845058-32b9d6a5da37?w=300"),
            ("Spinach", 3.49, "Vegetables", "https://images.unsplash.com/photo-1576045057995-568f588f82fb?w=300"),
            ("Tomatoes", 5.49, "Vegetables", "https://images.unsplash.com/photo-1546470427-0d4db154ceb8?w=300"),
            ("Potatoes", 4.99, "Vegetables", "https://images.unsplash.com/photo-1518977676601-b53f82ber630?w=300"),
            ("Whole Milk 2L", 3.99, "Dairy", "https://images.unsplash.com/photo-1563636619-e9143da7973b?w=300"),
            ("Cheddar Cheese", 7.49, "Dairy", "https://images.unsplash.com/photo-1618164436241-4473940d1f5c?w=300"),
            ("Greek Yoghurt", 5.99, "Dairy", "https://images.unsplash.com/photo-1488477181946-6428a0291777?w=300"),
            ("Chicken Breast 1kg", 12.99, "Meat", "https://images.unsplash.com/photo-1604503468506-a8da13d82791?w=300"),
            ("Beef Mince 500g", 9.99, "Meat", "https://images.unsplash.com/photo-1602470520998-f4a52199a3d6?w=300"),
            ("Salmon Fillet", 14.99, "Meat", "https://images.unsplash.com/photo-1574781330855-d0db8cc6a79c?w=300"),
            ("Sourdough Loaf", 6.50, "Bakery", "https://images.unsplash.com/photo-1509440159596-0249088772ff?w=300"),
            ("Croissants 4pk", 5.99, "Bakery", "https://images.unsplash.com/photo-1555507036-ab1f4038024a?w=300"),
            ("Orange Juice 1L", 4.49, "Beverages", "https://images.unsplash.com/photo-1621506289937-a8e4df240d0b?w=300"),
            ("Sparkling Water 6pk", 7.99, "Beverages", "https://images.unsplash.com/photo-1523362628745-0c100150b504?w=300"),
            ("Mixed Nuts 400g", 8.99, "Snacks", "https://images.unsplash.com/photo-1536816579748-4ecb3f03d72a?w=300"),
            ("Dark Chocolate Bar", 4.49, "Snacks", "https://images.unsplash.com/photo-1548907040-4baa42d10919?w=300"),
            ("Frozen Pizza", 8.99, "Frozen", "https://images.unsplash.com/photo-1513104890138-7c749659a591?w=300"),
            ("Ice Cream 1L", 7.49, "Frozen", "https://images.unsplash.com/photo-1497034825429-c343d7c6a68f?w=300"),
        ]

        for name, price, category_name, image_url in products_data:
            category = Category.objects.get(name=category_name)
            Product.objects.get_or_create(
                name=name,
                defaults={"price": price, "category": category, "image_url": image_url},
            )

        self.stdout.write(f"  Created {len(products_data)} products")

    def _create_inventory(self):
        import random
        stores = Store.objects.all()
        products = Product.objects.all()
        count = 0

        for product in products:
            for store in stores:
                _, created = PerStoreProduct.objects.get_or_create(
                    product=product,
                    store=store,
                    defaults={"quantity": random.randint(0, 50)},
                )
                if created:
                    count += 1

        self.stdout.write(f"  Created {count} inventory entries across {stores.count()} stores")
