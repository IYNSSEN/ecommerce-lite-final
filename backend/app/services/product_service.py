from app.repositories.product_repository import ProductRepository
from app.utils.errors import ValidationError, NotFoundError
from app.utils.cache import get_cache, set_cache, invalidate_prefix


class ProductService:
    def __init__(self):
        self.products = ProductRepository()

    def list_products(self, search=None):
        cache_key = f"products:list:{search or ''}"
        cached = get_cache(cache_key)
        if cached is not None:
            return cached, True

        products = [p.to_dict() for p in self.products.list(search=search)]
        set_cache(cache_key, products, ttl_seconds=60)
        return products, False

    def get_product(self, product_id):
        product = self.products.get_by_id(product_id)
        if not product:
            raise NotFoundError("Product not found")
        return product.to_dict()

    def create_product(self, data):
        clean = self._validate_product(data, partial=False)
        product = self.products.create(clean)
        invalidate_prefix("products:")
        return product.to_dict()

    def update_product(self, product_id, data):
        product = self.products.get_by_id(product_id)
        if not product:
            raise NotFoundError("Product not found")
        clean = self._validate_product(data, partial=True)
        product = self.products.update(product, clean)
        invalidate_prefix("products:")
        return product.to_dict()

    def delete_product(self, product_id):
        product = self.products.get_by_id(product_id)
        if not product:
            raise NotFoundError("Product not found")
        self.products.delete(product)
        invalidate_prefix("products:")

    def _validate_product(self, data, partial=False):
        errors = []
        clean = {}

        if not partial or "name" in data:
            name = (data.get("name") or "").strip()
            if not name:
                errors.append({"field": "name", "message": "Product name is required"})
            elif len(name) > 160:
                errors.append({"field": "name", "message": "Product name is too long"})
            else:
                clean["name"] = name

        if "description" in data:
            clean["description"] = (data.get("description") or "").strip()

        if not partial or "price" in data:
            try:
                price = float(data.get("price"))
                if price < 0:
                    raise ValueError()
                clean["price"] = price
            except (TypeError, ValueError):
                errors.append({"field": "price", "message": "Price must be a non-negative number"})

        if not partial or "stock" in data:
            try:
                stock = int(data.get("stock"))
                if stock < 0:
                    raise ValueError()
                clean["stock"] = stock
            except (TypeError, ValueError):
                errors.append({"field": "stock", "message": "Stock must be a non-negative integer"})

        if "active" in data:
            clean["active"] = bool(data.get("active"))

        if errors:
            raise ValidationError(details=errors)

        return clean
