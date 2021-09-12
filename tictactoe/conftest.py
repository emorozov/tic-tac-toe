import pytest
from rest_framework.test import APIClient


@pytest.fixture()
def client() -> APIClient:
    """Overrides pytest-django client with DRF test client."""
    return APIClient()
