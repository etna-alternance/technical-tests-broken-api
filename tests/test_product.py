import pytest
import requests


@pytest.fixture
def wipe(api_url: str):
    yield
    ps = requests.get(f"{api_url}/products").json()
    for p in ps:
        requests.delete(f"{api_url}/product/{p['id']}").raise_for_status()


def test_simple_create_and_delete(api_url: str):
    # Create a product
    p = {
        "name": "test",
        "price": 10,
        "type": "clothing",
    }
    resp = requests.post(f"{api_url}/product", json=p)
    assert resp.status_code == 201
    json = resp.json()
    assert p["name"] == json["name"] and p["price"] == json["price"] and p["type"] == json["type"]
    product_id = json["id"]

    # Check that it can be retrieved
    resp = requests.get(f"{api_url}/product/{product_id}")
    assert resp.json() == json

    # Delete the product
    resp = requests.delete(f"{api_url}/product/{product_id}")
    assert resp.status_code == 200


def test_list_all_products(api_url: str):
    resp = requests.get(f"{api_url}/products")
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)


def test_list_product_by_type(api_url: str, wipe):
    # Create dummy products
    for i in range(1, 4):
        resp = requests.post(f"{api_url}/product", json={"name": f"Lamp {i}", "price": i * 10, "type": "lighting"})
        assert resp.status_code == 201
        resp = requests.post(f"{api_url}/product", json={"name": f"Chair {i}", "price": i * 15, "type": "furniture"})
        assert resp.status_code == 201

    resp = requests.get(f"{api_url}/products", params={"type": "lighting"})
    json = resp.json()
    assert isinstance(json, list)
    assert len(json) == 3


def test_list_product_cheaper_than(api_url: str, wipe):
    # Create dummy products
    for i in range(1, 4):
        resp = requests.post(f"{api_url}/product", json={"name": f"Lamp {i}", "price": i * 10, "type": "lighting"})
        assert resp.status_code == 201
        resp = requests.post(f"{api_url}/product", json={"name": f"Chair {i}", "price": i * 15, "type": "furniture"})
        assert resp.status_code == 201

    resp = requests.get(f"{api_url}/products", params={"cheaper_than": 30})
    json = resp.json()
    assert isinstance(json, list)
    assert len(json) == 3
