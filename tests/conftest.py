import pytest

from .config import get_config


@pytest.fixture(scope="session")
def api_url() -> str:
    config = get_config()
    return f"http://{config.host}:{config.port}"
