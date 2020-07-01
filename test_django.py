from number_generation.models import Game


def test_create_game(driver, create_game):
    assert '/games/1' in driver.current_url
    games = Game.objects.filter(pk=1)
    game = games[0]
    winning_num = game.winning_num
    assert winning_num in range(game.lower_bound, game.upper_bound)
