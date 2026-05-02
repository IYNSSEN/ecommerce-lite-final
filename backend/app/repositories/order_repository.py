from app.models import db, Product, Order, OrderItem


class OrderRepository:
    def create_order(self, user_id, items):
        order = Order(user_id=user_id, status="created", total=0.0)
        db.session.add(order)

        total = 0.0
        for item in items:
            product = Product.query.get(item["productId"])
            quantity = item["quantity"]
            product.stock -= quantity
            order_item = OrderItem(
                order=order,
                product_id=product.id,
                quantity=quantity,
                unit_price=product.price
            )
            total += product.price * quantity
            db.session.add(order_item)

        order.total = total
        db.session.commit()
        return order

    def list_for_user(self, user_id):
        return Order.query.filter_by(user_id=user_id).order_by(Order.created_at.desc()).all()

    def list_all(self):
        return Order.query.order_by(Order.created_at.desc()).all()
