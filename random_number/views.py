from django.shortcuts import render
from random import randint


def homepage(request):
    return render(request, "index.html")


def guess_msg(request):
    guessed_number = request.POST['guess']
    random_number = randint(0, 100)
    if guessed_number == random_number:
        text = "Sucess! You have properly guessed the number"
    else:
        text = "Sorry, that's not right. Try Again!"
    context = {
        'response-text': text
    }
    return render(request, "message.html", context)
