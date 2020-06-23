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
    with webdriver.Chrome(chrome_options=driver_options) as driver:
        yield driver


def test_landing_page(driver, live_server, welcome):
    driver.get(live_server.url)
    # Find an input element
    input = driver.find_element_by_css_selector("#user-guess")
    submit = driver.find_element_by_css_selector(".submit-btn")
    if input is not None and submit is not None:
        assert True
    else:
        assert False
