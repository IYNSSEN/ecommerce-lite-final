from flask import Blueprint, request, jsonify, g
from app.services.order_service import OrderService
from app.utils.jwt_utils import require_auth, require_role

order_bp = Blueprint("orders", __name__)
service = OrderService()


@order_bp.post("/orders")
@require_auth
def create_order():
    return jsonify(service.create_order(g.current_user.id, request.get_json(silent=True) or {})), 201


@order_bp.get("/orders/my")
@require_auth
def my_orders():
    return jsonify({"items": service.list_my_orders(g.current_user.id)}), 200


@order_bp.get("/admin/orders")
@require_role("admin")
def admin_orders():
    return jsonify({"items": service.list_all_orders()}), 200
