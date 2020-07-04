from datetime import datetime
from number_generation.models import Game, Guess


def test_create_game(driver, create_game):
    assert '/games/1' in driver.current_url
    games = Game.objects.filter(pk=1)
    game = games[0]
    winning_num = game.winning_num
    assert winning_num in range(game.lower_bound, game.upper_bound)


def test_game_in_progress(driver, create_game):
    assert driver.find_element_by_css_selector('.in-progress')
    assert driver.find_element_by_css_selector('.previous-guesses')


def test_incorrect_guess(driver, create_game, make_guess):
    make_guess('120')
    make_guess('300')
    make_guess('500')
    elements = driver.find_elements_by_css_selector('.guess-item')
    element_text = []
    for element in elements:
        element_text_unfixed = element.text.split('-')[0]
        element_text_fin = element_text_unfixed.strip()
        element_text.append(element_text_fin)
    assert '120' in element_text


def test_correct_guess(driver, make_winning_game, get_primary_key, format_date):
    primary_key = get_primary_key()
    make_winning_game(primary_key)
    assert driver.find_element_by_css_selector('.finished')
    submit_button = driver.find_element_by_css_selector('.submit-button')
    my_game = Game.objects.filter(pk=primary_key)[0]
    assert submit_button.get_attribute('disabled')
    assert my_game.in_progress is not True
    displayed_guess = driver.find_element_by_css_selector('.winning-guess')
    formatted_date = format_date(my_game)
    assert formatted_date in displayed_guess.text
    assert str(my_game.winning_num) in displayed_guess.text


def test_game_page(
    driver,
    make_winning_game,
    get_primary_key,
    format_date
):
    primary_key = get_primary_key()
    make_winning_game(primary_key)
    back_button = driver.find_element_by_css_selector('.return-btn')
    back_button.click()
    game_row = driver.find_element_by_css_selector('.game-item')
    completion_status = game_row.find_element_by_css_selector('.completion')      
    my_game = Game.objects.filter(pk=primary_key)[0]
    assert 'Completed' in completion_status.text
    winning_guess = game_row.find_element_by_css_selector('.winning-guess')
    assert str(my_game.winning_num) in winning_guess.text
    formatted_date = format_date(my_game)
    assert formatted_date in winning_guess.text
