from django.shortcuts import render
from random import randint


def homepage(request):
    return render(request, "index.html")


def guess_msg(request):
    min_number = int(request.POST['min-num'])
    max_number = int(request.POST['max-num'])
    guessed_number = int(request.POST['guess'])
    if guessed_number < min_number or guessed_number > max_number:
        text = "The number is out of bounds. Please choose another number"
        context = {'response': text}
        return render(request, "message.html", context)
    random_number = randint(min_number, max_number)
    if guessed_number == random_number:
        text = "Success! You have properly guessed the number"
    else:
        text = "Sorry, that's not right. Try Again!"
    context = {'response': text}
    print(context)
    return render(request, "message.html", context)
