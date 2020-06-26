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
    min_label = driver.find_element_by_css_selector('.min-num-lab')
    max_label = driver.find_element_by_css_selector('.max-num-lab')
    if user_label is not None and min_label is not None and \
       max_label is not None:
        assert True
    else:
        assert False


def test_guess_random_number(driver, live_server):
    driver.get(live_server.url)
    min_input = driver.find_element_by_css_selector('.min-level')
    min_input.send_keys('1')
    max_input = driver.find_element_by_css_selector('.max-level')
    max_input.send_keys('10')
    user_input = driver.find_element_by_css_selector('.user-guess')
    user_input.send_keys('5')
    submit_button = driver.find_element_by_css_selector('.submit-btn')
    submit_button.click()
    response_message = driver.find_element_by_css_selector('.response-message')
    response_message = response_message.text
    assert 'success' in response_message.lower() or \
        'sorry' in response_message.lower()


def test_try_again(driver, live_server):
    driver.get(live_server.url)
    min_input = driver.find_element_by_css_selector('.min-level')
    min_input.send_keys('1')
    max_input = driver.find_element_by_css_selector('.max-level')
    max_input.send_keys('10')
    user_input = driver.find_element_by_css_selector('.user-guess')
    user_input.send_keys('5')
    submit_button = driver.find_element_by_css_selector('.submit-btn')
    submit_button.click()
    # Find the try again button
    try_again_button = driver.find_element_by_css_selector('.try-again')
    try_again_button.click()
    # Check inputs again
    user_label = driver.find_element_by_css_selector('.user-label')
    if user_label is not None:
        assert True
    else:
        assert False


def test_limits(driver, live_server):
    driver.get(live_server.url)
    min_input = driver.find_element_by_css_selector('.min-level')
    min_input.send_keys('1')
    max_input = driver.find_element_by_css_selector('.max-level')
    max_input.send_keys('10')
    user_input = driver.find_element_by_css_selector('.user-guess')
    user_input.send_keys('123')
    submit_button = driver.find_element_by_css_selector('.submit-btn')
    submit_button.click()
    response_message = driver.find_element_by_css_selector('.response-message')
    assert 'choose another number' in response_message.text.lower()
