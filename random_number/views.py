from django.shortcuts import render, redirect, get_object_or_404
from number_generation.models import Game, Guess
from random import randint
from django.contrib.auth import authenticate, login, logout


def homepage(request):
    return render(request, 'index.html')


def games(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            user = request.user
        else:
            return redirect('/login')
        lower = request.POST['min-num']
        upper = request.POST['max-num']
        if lower > upper:
            error_message = "Please choose correct bounds. Your lower bound is greater than upper bound"
            context = {'error': error_message}
            return render(request, 'bound_error.html', context=context)
        else:
            winning_number = randint(int(lower), int(upper))
            new_game = Game.objects.create(
                lower_bound=lower, upper_bound=upper, winning_num=winning_number, created_by=user)
            # Redirect to this url
            return redirect(f'/games/{new_game.pk}')
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
            'games_guesses': game_and_guess,
            'user': user
        }
        return render(request, 'games.html', context=context)


def game(request, game_num):
    winning_guess = ''
    my_game = get_object_or_404(Game, pk=game_num)
    if request.method == 'POST':
        if request.user.is_authenticated:
            user = request.user
            guess_val = int(request.POST['guess-value'])
            new_guess = Guess(guess_value=guess_val, game=my_game, created_by=user)
            if guess_val == my_game.winning_num:
                my_game.in_progress = False
                winning_guess = new_guess
            my_game.save()
            new_guess.save()
        else:
            error_message = 'You must be logged in to complete that action'
            context = {'error': error_message}
            return render(request, 'non_user_error.html', context)
    guesses = Guess.objects.filter(game=my_game)
    context = {
        'game': my_game,
        'gamepk': my_game.pk,
        'guesses': guesses,
        'winning_guess': winning_guess,
    }
    return render(request, 'game.html', context)


def log_in(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect('/')
    return render(request, 'login.html')


def log_out(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('log_in')
