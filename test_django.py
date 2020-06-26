import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


@pytest.yield_fixture
def driver():
    driver_options = Options()
    driver_options.add_argument("--no-sandbox")
    driver_options.add_argument("--disable-dev-shm-usage")
    driver_options.add_argument("--headless")
    with webdriver.Chrome(chrome_options=driver_options) as driver:
        yield driver


def test_landing_page(driver, live_server):
    driver.get(live_server.url)
    # Find an input element
    user_input = driver.find_element_by_css_selector("input.user-guess")
    submit = driver.find_element_by_css_selector(".submit-btn")
    if user_input is not None and submit is not None:
        assert True
    else:
        assert False


def test_check_label(driver, live_server):
    driver.get(live_server.url)
    user_label = driver.find_element_by_css_selector('.user-label')
    if user_label is not None:
        assert True
    else:
        assert False


def test_guess_random_number(driver, live_server):
    driver.get(live_server.url)
    user_input = driver.find_element_by_css_selector('.user-guess')
    user_input.send_keys('12')
    submit_button = driver.find_element_by_css_selector('.submit-btn')
    submit_button.click()
    response_message = driver.find_element_by_css_selector('.response-message')
    assert 'success' in response_message.lower() or \
        'sorry' in response_message.lower()
