import pytest

from app import app as application


@pytest.fixture
def app():
    return application
