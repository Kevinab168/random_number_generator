from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    pass


class Game(models.Model):
    lower_bound = models.IntegerField(default=0)
    upper_bound = models.IntegerField(default=0)
    in_progress = models.BooleanField(default='True')
    winning_num = models.IntegerField(default=0)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)


class Guess(models.Model):
    guess_value = models.IntegerField(default=0)
    guess_date = models.DateTimeField(auto_now=True)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
