import pytest

@pytest.fixture(scope="session")
def sample_data():
    """Fixture for sample data used in tests."""
    return {"user": "test-user", "product": "test-product"}
