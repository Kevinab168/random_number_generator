from django.shortcuts import render, redirect, get_object_or_404
from number_generation.models import Game, Guess
from random import randint


def homepage(request):
    return render(request, "index.html")


def games(request):
    if request.method == "POST":
        lower = request.POST['min-num']
        upper = request.POST['max-num']
        winning_number = randint(int(lower), int(upper))
        new_game = Game(lower_bound=lower, upper_bound=upper, winning_num=winning_number)
        new_game.save()

        # Redirect to this url
        return redirect(f'games/{new_game.pk}')
    else:
        all_games = Game.objects.all()
        game_and_guess = []
        for game in all_games:
            winning_guess = Guess.objects.filter(game=game, guess_value=game.winning_num)
            if winning_guess:
                game_and_guess.append((game, winning_guess))
            else:
                game_and_guess.append((game, '?'))
        context = {
            'games_guesses': game_and_guess
        }
        return render(request, 'games.html', context=context)


def game(request, game_num):
    my_game = get_object_or_404(Game, pk=game_num)
    if request.method == 'POST':
        guess_val = int(request.POST['guess-value'])
        if guess_val == my_game.winning_num:
            my_game.in_progress = False
        new_guess = Guess(guess_value=guess_val, game=my_game)
        my_game.save()
        new_guess.save()
    print(my_game.in_progress)
    guesses = Guess.objects.filter(game=my_game)
    context = {
        'game': my_game,
        'gamepk': my_game.pk,
        'guesses': guesses
    }
    return render(request, 'game.html', context)
