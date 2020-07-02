from django.db import models
from random import randint


class Game(models.Model):
    lower_bound = models.IntegerField(default=0)
    upper_bound = models.IntegerField(default=0)
    in_progress = models.BooleanField(default="True")

    @property
    def winning_num(self):
        return randint(self.lower_bound, self.upper_bound)


class Guess(models.Model):
    guess_value = models.IntegerField(default=0)
    guess_date = models.DateTimeField(auto_now=True)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
