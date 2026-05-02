from app.models import Product, db


class ProductRepository:
    def list(self, search=None, active_only=True):
        query = Product.query
        if active_only:
            query = query.filter(Product.active.is_(True))
        if search:
            like = f"%{search}%"
            query = query.filter(Product.name.ilike(like))
        return query.order_by(Product.id.asc()).all()

    def get_by_id(self, product_id):
        return Product.query.get(product_id)

    def create(self, data):
        product = Product(**data)
        db.session.add(product)
        db.session.commit()
        return product

    def update(self, product, data):
        for key, value in data.items():
            setattr(product, key, value)
        db.session.commit()
        return product

    def delete(self, product):
        db.session.delete(product)
        db.session.commit()
