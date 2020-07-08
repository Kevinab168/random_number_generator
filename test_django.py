from number_generation.models import Game, Guess


def test_log_in(driver, live_server, login, user):
    new_user = user('User', 'asdfjkasdf;lasdf')
    login(new_user, password='asdfjkasdf;lasdf')
    assert driver.current_url == live_server.url + '/'
    assert new_user.username in driver.page_source


def test_log_out(driver, login, user):
    new_user = user('User', 'asdfjkasdf;lasdf')
    login(new_user, password='asdfjkasdf;lasdf')
    logout = driver.find_element_by_css_selector('[data-test="logout"]')
    logout.click()
    assert 'login/' in driver.current_url
    assert new_user.username not in driver.page_source


def test_create_game_non_user(driver, create_game):
    create_game()
    assert 'login/' in driver.current_url


def test_create_game(driver, create_game, login, user):
    new_user = user('User', 'asdfjkasdf;lasdf')
    login(new_user, password='asdfjkasdf;lasdf')
    create_game()
    assert '/games/1' in driver.current_url
    game = Game.objects.all().last()
    assert game.winning_num in range(game.lower_bound, game.upper_bound)
    creator = driver.find_element_by_css_selector('[data-test="creator"]')
    assert creator.text == game.created_by.username
    assert driver.find_element_by_css_selector('[data-test="in-progress"]')
    assert driver.find_element_by_css_selector('[data-test="previous-guesses"]')


def test_create_game_incorrect_bounds(driver, live_server, create_game, login, user):
    new_user = user('User', 'asdfjkasdf;lasdf')
    login(new_user, password='asdfjkasdf;lasdf')
    create_game(lower=100, upper=1)
    error_message = driver.find_element_by_css_selector('[data-test="error-message').text
    assert 'lower bound is greater than upper bound' in error_message
    home_button = driver.find_element_by_css_selector('[data-test="home-button"]')
    home_button.click()
    assert driver.current_url == live_server.url + '/'


def test_incorrect_guess(driver, create_game, login, user, make_guess):
    new_user = user('User', 'asdfjkasdf;lasdf')
    login(new_user, password='asdfjkasdf;lasdf')
    create_game(1, 100)
    game = Game.objects.all().last()
    winning_number = game.winning_num
    guess_number = 43
    if guess_number != winning_number:
        make_guess(guess_number)
    else:
        guess_number = guess_number + 1
        make_guess(guess_number)
    guess = Guess.objects.all().last()
    element = driver.find_element_by_css_selector('[data-test="incorrect-guess"]')
    assert str(guess_number) in element.text
    author_by = driver.find_element_by_css_selector('[data-test="author"]')
    assert author_by.text == guess.created_by.username


def test_make_guess_non_user(driver, live_server, create_game, login, user, make_guess):
    new_user = user('User', 'asdfjkasdf;lasdf')
    login(new_user, password='asdfjkasdf;lasdf')
    create_game()
    game = Game.objects.all().last()
    logout = driver.find_element_by_css_selector('[data-test="logout"]')
    logout.click()
    driver.get(live_server + f'/games/{game.pk}')
    make_guess(23)
    error_message = driver.find_element_by_css_selector('[data-test="error-message"]')
    assert 'must be logged in' in error_message.text
    log_in_button = driver.find_element_by_css_selector('[data-test="log-in-button"]')
    log_in_button.click()
    assert 'login/' in driver.current_url


def test_correct_guess(driver, create_game, make_guess, login, format_date, user):
    new_user = user('User', 'asdfjkasdf;lasdf')
    login(new_user, password='asdfjkasdf;lasdf')
    create_game(1, 100)
    game = Game.objects.all().last()
    winning_number = game.winning_num
    make_guess(winning_number)
    winning_guess = Guess.objects.all().last()
    displayed_winning_number = driver.find_element_by_css_selector('[data-test="winning-guess-item"]')
    assert displayed_winning_number.text == str(winning_number)
    displayed_winning_author = driver.find_element_by_css_selector('[data-test="winning-author"]').text
    assert winning_guess.created_by.username == displayed_winning_author
    displayed_winning_date = driver.find_element_by_css_selector('[data-test="winning-date"').text
    formatted_date = format_date(winning_guess)
    assert formatted_date in displayed_winning_date


def test_show_all_games(driver, live_server, create_game, login, user):
    new_user = user('User', 'asdfjkasdf;lasdf')
    login(new_user, password='asdfjkasdf;lasdf')
    create_game()
    game = Game.objects.all().last()
    driver.get(live_server.url)
    show_all_games_button = driver.find_element_by_css_selector('[data-test="show_all_games"]')
    show_all_games_button.click()
    game_link = driver.find_element_by_css_selector('[data-test="game-name"]')
    assert driver.find_element_by_css_selector('[data-test="game-progress"]')
    game_link.click()
    assert str(game.pk) in driver.current_url
