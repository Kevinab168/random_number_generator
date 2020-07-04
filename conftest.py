import os
import re
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from number_generation.models import Game


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
def create_game(driver, live_server, transactional_db):
    driver.get(live_server.url)
    lower_bound = driver.find_element_by_css_selector('.lower-bound')
    upper_bound = driver.find_element_by_css_selector('.upper-bound')
    lower_bound.send_keys('1')
    upper_bound.send_keys('100')

    create_game = driver.find_element_by_css_selector('.create-game')
    create_game.click()


@pytest.fixture
def make_guess(driver, live_server):
    def guess_it(value):
        guess = driver.find_element_by_css_selector('.guess-number')
        guess.send_keys(value)
        submit = driver.find_element_by_css_selector('.submit-button')
        submit.click()
    return guess_it


@pytest.fixture
def get_primary_key(driver, live_server):
    def action():
        current_url = driver.current_url
        pattern = r'.*games/([0-9]+)'
        values = re.search(pattern, current_url)
        my_pk = values.group(1)
        return my_pk
    return action


@pytest.fixture
def make_winning_game(driver, live_server, create_game, make_guess):
    def action(winning_pk):
        my_game = Game.objects.filter(pk=winning_pk)[0]
        winning_number = my_game.winning_num
        make_guess(winning_number)
    return action
