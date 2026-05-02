from app import create_app


def test_health_endpoint():
    app = create_app()
    client = app.test_client()
    res = client.get("/health")
    assert res.status_code == 200
    assert res.json["status"] == "ok"


def test_products_endpoint():
    app = create_app()
    client = app.test_client()
    res = client.get("/api/v1/products")
    assert res.status_code == 200
    assert "items" in res.json
