from app.models import Product
from app.repositories.order_repository import OrderRepository
from app.utils.errors import ValidationError, NotFoundError


class OrderService:
    def __init__(self):
        self.orders = OrderRepository()

    def create_order(self, user_id, data):
        raw_items = data.get("items") or []
        if not isinstance(raw_items, list) or len(raw_items) == 0:
            raise ValidationError(details=[{"field": "items", "message": "Order must contain at least one item"}])

        items = []
        errors = []
        for idx, item in enumerate(raw_items):
            try:
                product_id = int(item.get("productId"))
                quantity = int(item.get("quantity", 1))
            except (TypeError, ValueError):
                errors.append({"field": f"items[{idx}]", "message": "productId and quantity must be numbers"})
                continue

            if quantity <= 0:
                errors.append({"field": f"items[{idx}].quantity", "message": "Quantity must be greater than 0"})
                continue

            product = Product.query.get(product_id)
            if not product or not product.active:
                raise NotFoundError(f"Product {product_id} not found")
            if product.stock < quantity:
                errors.append({"field": f"items[{idx}].quantity", "message": f"Not enough stock for product {product_id}"})
                continue

            items.append({"productId": product_id, "quantity": quantity})

        if errors:
            raise ValidationError(details=errors)

        order = self.orders.create_order(user_id, items)
        return order.to_dict()

    def list_my_orders(self, user_id):
        return [order.to_dict() for order in self.orders.list_for_user(user_id)]

    def list_all_orders(self):
        return [order.to_dict() for order in self.orders.list_all()]
