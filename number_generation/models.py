from django.db import models
from random import randint


class Game(models.Model):
    lower_bound = models.IntegerField(default=0)
    upper_bound = models.IntegerField(default=0)

    @property
    def winning_num(self):
        return randint(self.lower_bound, self.upper_bound)
