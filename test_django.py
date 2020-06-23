import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


@pytest.fixture
def welcome():
    return "welcome"


@pytest.yield_fixture
def driver():
    driver_options = Options()
    driver_options.add_argument("--no-sandbox")
    driver_options.add_argument("--disable-dev-shm-usage")
    driver_options.add_argument("--headless")
    with webdriver.Remote(driver_options) as driver:
        yield driver


def test_landing_page(driver, live_server, welcome):
    driver.get(live_server.url)
    assert welcome in driver.page_source
