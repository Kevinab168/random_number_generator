import re
from number_generation.models import Game


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


def test_correct_guess(driver, create_game, get_primary_key, make_guess):
    primary_key = get_primary_key()
    my_game = Game.objects.filter(pk=primary_key)[0]
    winning_number = my_game.winning_num
    make_guess(winning_number)
    assert driver.find_element_by_css_selector('.finished')
    submit_button = driver.find_element_by_css_selector('.submit-button')
    my_game = Game.objects.filter(pk=primary_key)[0]
    assert submit_button.get_attribute('disabled')
    assert my_game.in_progress is not True
