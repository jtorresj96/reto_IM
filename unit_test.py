import pytest
from fastapi.testclient import TestClient
from main import app, SECRET_KEY, ALGORITHM
import jwt
import datetime
from typing import Any, Dict, List, Optional

client: TestClient = TestClient(app)

def generate_token(username: str, hours_valid: int = 1) -> str:
    exp: datetime.datetime = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=hours_valid)
    token: Any = jwt.encode({"sub": username, "exp": exp}, SECRET_KEY, algorithm=ALGORITHM)
    if isinstance(token, bytes):
        token = token.decode("utf-8")
    return token

def fake_get_all_products(min_price: float, max_price: float) -> List[Dict[str, Any]]:
    return [{"id": 1, "name": "Producto 1", "price": 10.0}]

def fake_get_product_by_id_found(product_id: int) -> Optional[Dict[str, Any]]:
    return {"id": 1, "name": "Producto 1", "price": 10.0}

def fake_get_product_by_id_not_found(product_id: int) -> Optional[Dict[str, Any]]:
    return None

def test_authenticate_user_success() -> None:
    response = client.post("/auth/", data={"username": "admin", "password": "imagemaker"})
    assert response.status_code == 200
    data: Dict[str, Any] = response.json()
    assert "access_token" in data
    token: str = data["access_token"]
    payload: Dict[str, Any] = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    assert payload["sub"] == "admin"

def test_authenticate_user_failure() -> None:
    response = client.post("/auth/", data={"username": "admin", "password": "wrongpassword"})
    assert response.status_code == 401

def test_get_products_no_auth() -> None:
    response = client.get("/products")
    assert response.status_code == 401

def test_get_products_success(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("main.client.get_all_products", fake_get_all_products)
    token: str = generate_token("admin")
    headers: Dict[str, str] = {"Authorization": f"Bearer {token}"}
    response = client.get("/products", headers=headers)
    assert response.status_code == 200
    assert response.json() == {"products": [{"id": 1, "name": "Producto 1", "price": 10.0}]}

def test_get_product_success(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("main.client.get_product_by_id", fake_get_product_by_id_found)
    token: str = generate_token("admin")
    headers: Dict[str, str] = {"Authorization": f"Bearer {token}"}
    response = client.get("/products/products_id", params={"product_id": 1}, headers=headers)
    assert response.status_code == 200
    assert response.json() == {"id": 1, "name": "Producto 1", "price": 10.0}

def test_get_product_not_found(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("main.client.get_product_by_id", fake_get_product_by_id_not_found)
    token: str = generate_token("admin")
    headers: Dict[str, str] = {"Authorization": f"Bearer {token}"}
    response = client.get("/products/products_id", params={"product_id": 1000000}, headers=headers)
    assert response.status_code == 404
