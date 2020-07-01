from django.shortcuts import render, redirect, get_object_or_404
from number_generation.models import Game


def homepage(request):
    return render(request, "index.html")


def games(request):
    if request.method == "POST":
        lower = request.POST['min-num']
        upper = request.POST['max-num']
        new_game = Game(lower_bound=lower, upper_bound=upper)
        new_game.save()

        # Redirect to this url
        return redirect(f'games/{new_game.pk}')


def game(request, game_num):
    my_game = get_object_or_404(Game, pk=game_num)
    context = {
        'game': my_game
    }
    return render(request, 'game.html', context)
