from rest_framework.test import APIClient
import pytest
from musicshop.main.models import Product


@pytest.mark.django_db
def test_product_list_api():
    client = APIClient()
    response = client.get("/v1/products/")
    assert response.status_code == 200
    assert "results" in response.data  # Для пагинированных ответов


@pytest.mark.django_db
def test_product_create_api():
    client = APIClient()
    data = {"name": "Новый", "price": 50}
    response = client.post("/v1/products/", data, format="json")
    assert response.status_code == 201
    assert Product.objects.count() == 1
