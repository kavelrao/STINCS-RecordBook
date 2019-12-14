from django.db import models
from django.contrib.auth.models import User

import os
from pathlib import Path


class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_captain = models.BooleanField(default=False)

    team = models.OneToOneField(
        'Team',
        on_delete=models.CASCADE,
        related_name='team',
    )

    def __str__(self):
        return self.user.username

class Team(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Design(models.Model):
    name = models.CharField(max_length=50)
    owner = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.name

    @property
    def filepath(self):
        path = str(Path().absolute().parent.absolute()) + "/media/" + self.owner.team.name
        return path
