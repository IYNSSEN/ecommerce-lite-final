import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import create_app
from app.models import db, User, Product

app = create_app()

with app.app_context():
    db.drop_all()
    db.create_all()

    admin = User(email="admin@example.com", role="admin")
    admin.set_password("admin123")

    user = User(email="user@example.com", role="user")
    user.set_password("user123")

    products = [
        Product(name="Laptop Basic", description="Affordable student laptop", price=2499.00, stock=8),
        Product(name="Wireless Mouse", description="USB wireless mouse", price=59.99, stock=30),
        Product(name="Mechanical Keyboard", description="Compact keyboard", price=199.00, stock=12),
        Product(name="USB-C Hub", description="Multi-port adapter", price=129.00, stock=15),
        Product(name="Noise Cancelling Headphones", description="Over-ear headphones", price=399.00, stock=6),
    ]

    db.session.add_all([admin, user] + products)
    db.session.commit()

    print("Seed completed.")
    print("Admin: admin@example.com / admin123")
    print("User:  user@example.com / user123")
