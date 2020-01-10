from django.db import models
from django.contrib.auth.models import User

import os
from pathlib import Path


class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_captain = models.BooleanField(default=False)

    team = models.ForeignKey(
        'Team',
        on_delete=models.CASCADE,
        related_name='accounts',
    )

    def __str__(self):
        return self.user.username

class Team(models.Model):
    name = models.CharField(max_length=50)
    join_code = models.CharField(max_length=8)

    def __str__(self):
        return self.name

class Design(models.Model):
    name = models.CharField(max_length=50)
    motor_diameter = models.IntegerField()  # millimeters
    fin_description = models.CharField(max_length=500)
    length = models.DecimalField(decimal_places=2, max_digits=6)  # millimeters
    diameter = models.DecimalField(decimal_places=2, max_digits=6)  # millimeters
    owner = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
        related_name='designs',
    )

    def __str__(self):
        return self.name

    @property
    def folderpath(self):
        path = str(Path().absolute().parent.absolute()) + "/media/" + self.owner.team.name + '/' + self.name
        return path
