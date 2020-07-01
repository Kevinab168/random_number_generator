import os
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


# @pytest.fixture
# def user_selects_between_1_and_10(driver, live_server):
#     driver.get(live_server.url)
#     min_input = driver.find_element_by_css_selector('.min-level')
#     min_input.send_keys('1')
#     max_input = driver.find_element_by_css_selector('.max-level')
#     max_input.send_keys('10')


# @pytest.fixture
# def user_send_keys(driver, live_server):
#     def action(value):
#         user_input = driver.find_element_by_css_selector('.user-guess')
#         user_input.send_keys(value)
#         submit_button = driver.find_element_by_css_selector('.submit-btn')
#         submit_button.click()
#     return action


@pytest.yield_fixture(scope='session')
def driver():
    if os.environ.get('CI'):
        driver_options = Options()
        driver_options.add_argument('--no-sandbox')
        driver_options.add_argument('--disable-dev-shm-usage')
        driver_options.add_argument('--headless')
        driver = webdriver.Chrome(chrome_options=driver_options)
    else:
        driver = webdriver.Remote(command_executor='http://127.0.0.1:9515')
    with driver:
        yield driver


@pytest.fixture(scope='function')
def create_game(driver, live_server, db):
    driver.get(live_server.url)
    lower_bound = driver.find_element_by_css_selector('.lower-bound')
    upper_bound = driver.find_element_by_css_selector('.upper-bound')
    lower_bound.send_keys('1')
    upper_bound.send_keys('100')

    create_game = driver.find_element_by_css_selector('.create-game')
    create_game.click()
