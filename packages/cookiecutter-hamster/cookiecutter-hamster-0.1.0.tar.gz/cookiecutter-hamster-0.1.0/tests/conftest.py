import pytest
from pytest_cookies.plugin import Cookies, Result


@pytest.fixture()
def default_project(cookies: Cookies) -> Result:
    return cookies.bake({
        "project_name": "salamander",
    })


@pytest.fixture()
def project_salaman(cookies: Cookies) -> Result:
    return cookies.bake({
        "project_name": "salaman",
        "db_name": "salaman",
    })
