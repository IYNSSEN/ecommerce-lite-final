from flask import Blueprint, request, jsonify
from app.services.product_service import ProductService
from app.utils.jwt_utils import require_role

product_bp = Blueprint("products", __name__)
service = ProductService()


@product_bp.get("")
def list_products():
    search = request.args.get("search")
    products, cache_hit = service.list_products(search=search)
    response = jsonify({"items": products, "cacheHit": cache_hit})
    response.headers["X-Cache"] = "HIT" if cache_hit else "MISS"
    return response, 200


@product_bp.get("/<int:product_id>")
def get_product(product_id):
    return jsonify(service.get_product(product_id)), 200


@product_bp.post("")
@require_role("admin")
def create_product():
    return jsonify(service.create_product(request.get_json(silent=True) or {})), 201


@product_bp.put("/<int:product_id>")
@require_role("admin")
def update_product(product_id):
    return jsonify(service.update_product(product_id, request.get_json(silent=True) or {})), 200


@product_bp.delete("/<int:product_id>")
@require_role("admin")
def delete_product(product_id):
    service.delete_product(product_id)
    return "", 204
