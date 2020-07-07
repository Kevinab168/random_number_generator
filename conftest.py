import os
import re
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from datetime import datetime
from number_generation.models import Game, Guess, User


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
def create_game(driver, live_server):
    def action(lower=1, upper=100):
        driver.get(live_server.url)
        lower_bound = driver.find_element_by_css_selector('[data-test="lower-bound"]')
        upper_bound = driver.find_element_by_css_selector('[data-test="upper-bound"]')
        lower_bound.send_keys(lower)
        upper_bound.send_keys(upper)

        create_game = driver.find_element_by_css_selector('[data-test="create-game"]')
        create_game.click()
    return action


@pytest.fixture
def login(driver, live_server):
    def action(user, password):
        driver.get(live_server.url + '/login')
        username = driver.find_element_by_css_selector('[data-test="username"]')
        username.send_keys(user.username)
        password = driver.find_element_by_css_selector('[data-test="password"]')
        password.send_keys('asdfjkasdf;lasdf')
        log_in = driver.find_element_by_css_selector('[data-test="login"')
        log_in.click()
    return action

@pytest.fixture
def make_guess(driver, live_server):
    def guess_it(value):
        guess = driver.find_element_by_css_selector('.guess-number')
        guess.send_keys(value)
        submit = driver.find_element_by_css_selector('.submit-button')
        submit.click()
    return guess_it


@pytest.fixture
def make_winning_game(driver, live_server, create_game, make_guess):
    def action(winning_pk):
        my_game = Game.objects.filter(pk=winning_pk)[0]
        winning_number = my_game.winning_num
        make_guess(winning_number)
    return action


@pytest.fixture
def format_date():
    def action(guess):
        formatted_date = datetime.strftime(guess.guess_date, '%B %d, %Y, %I:%M').lstrip('0').replace(' 0', ' ')
        formatted_date = formatted_date.replace(':00', '')
        return formatted_date
    return action


@pytest.fixture
def user():
    def action(username, password):
        new_user = User.objects.create_user(username=username, password=password)
        return new_user
    return action
