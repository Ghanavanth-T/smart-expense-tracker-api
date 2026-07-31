def test_list_is_empty_initially(client):
    response = client.get("/expenses")
    assert response.status_code == 200
    assert response.json() == []

def test_create_expense_lowercases_category(client):
    response = client.post(
        "/expenses",
        json={
            "title": "Groceries",
            "amount": 250.50,
            "category": "FOOD",
            "date": "2026-07-30",
        },
    )

    assert response.status_code == 201
    assert response.json()["category"] == "food"

def test_create_expense_returns_201_with_generated_id(client):
    response = client.post(
        "/expenses",
        json={
            "title": "Groceries",
            "amount": 250.50,
            "category": "FOOD",
            "date": "2026-07-30",
        },
    )

    body = response.json()
    assert response.status_code == 201
    assert body["id"]

def test_create_expense_rejects_negative_amount(client):
    response = client.post(
        "/expenses",
        json={
            "title": "Groceries",
            "amount": -250.50,
            "category": "FOOD",
            "date": "2026-07-30",
        },
    )

    assert response.status_code == 422
    assert response.json()["detail"][0]["loc"] == ["body", "amount"]

def test_filter_returns_only_matching_category(client):
    client.post("/expenses", json={
        "title": "Groceries", "amount": 250.50,
        "category": "FOOD", "date": "2026-07-30",
    })
    client.post("/expenses", json={
        "title": "Bus pass", "amount": 900,
        "category": "transport", "date": "2026-07-29",
    })

    response = client.get("/expenses?category=food")

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["category"] == "food"

def test_summary_totals_overall_and_by_category(client):
    client.post(
        "/expenses",
        json={
            "title": "Groceries",
            "amount": 250.50,
            "category": "FOOD",
            "date": "2026-07-30",
        },
    )
    client.post(
        "/expenses",
        json={
            "title": "Lunch", "amount": 120.30,
            "category": "food", "date": "2026-07-29",
        },
    )

    response = client.get("/expenses/summary")

    assert response.status_code == 200
    assert response.json() == {
        "total": 370.80,
        "by_category": {"food": 370.80},
    }

def test_delete_removes_expense(client):
    response = client.post(
        "/expenses",
        json={
            "title": "Groceries",
            "amount": 250.50,
            "category": "FOOD",
            "date": "2026-07-30",
        },
    )
    expense_id = response.json()["id"]

    response = client.delete(f"/expenses/{expense_id}")
    assert response.status_code == 200
    assert response.json() == {"message": "Expense deleted successfully"}

    response = client.get("/expenses")
    assert response.json() == []

def test_delete_unknown_id_returns_404(client):
    response = client.delete("/expenses/non-existent-id")
    assert response.status_code == 404
    