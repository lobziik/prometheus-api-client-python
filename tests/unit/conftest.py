import pytest


@pytest.fixture(scope='module', autouse=True)
def mock_all_http():
    yield
