def test_create_item(client):
    response = client.post("/items/", json={"name": "Laptop", "price": 999.99})
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Laptop"
    assert data["price"] == 999.99
    assert "id" in data


def test_get_item(client):
    # Сначала создаем товар
    create_response = client.post("/items/", json={"name": "Phone", "price": 599.99})
    item_id = create_response.json()["id"]
    
    # Получаем товар по ID
    response = client.get(f"/items/{item_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Phone"
    assert data["id"] == item_id


def test_get_item_not_found(client):
    response = client.get("/items/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Item not found"