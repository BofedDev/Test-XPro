def make_category(client, **kw):
    r = client.post("/categories/", json={"name": "Cat", **kw})
    assert r.status_code == 201, r.text
    return r.json()


def test_health(client):
    assert client.get("/health").json() == {"status": "ok"}


def test_category_crud(client):
    c = make_category(client, meta_title="T")
    assert c["meta_title"] == "T"
    cid = c["category_id"]

    assert client.get(f"/categories/{cid}").status_code == 200
    r = client.put(f"/categories/{cid}", json={"name": "New"})
    assert r.json()["name"] == "New"
    assert client.delete(f"/categories/{cid}").status_code == 204
    assert client.get(f"/categories/{cid}").status_code == 404


def test_category_unknown_parent_and_self_parent(client):
    r = client.post("/categories/", json={"name": "x", "parent_category_id": 999})
    assert r.status_code == 400
    cid = make_category(client)["category_id"]
    r = client.put(f"/categories/{cid}", json={"parent_category_id": cid})
    assert r.status_code == 409


def test_cannot_delete_category_with_children(client):
    parent = make_category(client)["category_id"]
    make_category(client, parent_category_id=parent)
    assert client.delete(f"/categories/{parent}").status_code == 409


def test_product_crud_with_sku(client):
    cid = make_category(client)["category_id"]
    r = client.post(
        "/products/",
        json={"name": "P", "price": "10.50", "sku": "A-1", "category_id": cid},
    )
    assert r.status_code == 201, r.text
    p = r.json()
    assert p["sku"] == "A-1"

    r = client.put(f"/products/{p['product_id']}", json={"quantity": 5})
    assert r.json()["quantity"] == 5
    assert len(client.get(f"/products/?category_id={cid}").json()) == 1
    assert client.delete(f"/products/{p['product_id']}").status_code == 204


def test_product_unknown_category(client):
    r = client.post("/products/", json={"name": "P", "price": 1, "category_id": 123})
    assert r.status_code == 400


def test_product_validation(client):
    assert client.post("/products/", json={"name": "P", "price": -1}).status_code == 422
    assert client.get("/products/?limit=0").status_code == 422


def test_deleting_category_unsets_product_category(client):
    cid = make_category(client)["category_id"]
    pid = client.post(
        "/products/", json={"name": "P", "price": 1, "category_id": cid}
    ).json()["product_id"]
    client.delete(f"/categories/{cid}")
    assert client.get(f"/products/{pid}").json()["category_id"] is None
