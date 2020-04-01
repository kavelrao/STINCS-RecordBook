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
    name = models.CharField(max_length=30)
    motor_diameter = models.IntegerField()  # millimeters
    fin_description = models.CharField(max_length=500)
    length = models.DecimalField(decimal_places=2, max_digits=6)  # millimeters
    diameter = models.DecimalField(decimal_places=2, max_digits=6)  # millimeters
    upload = models.FileField(upload_to='media/', default=None)
    owner = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
        related_name='designs',
    )
    team = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        related_name='designs',
    )

    def __str__(self):
        return self.name

    @property
    def folderpath(self):
        path = str(Path().absolute().absolute()) + "/media/" + self.owner.team.name + '/' + self.name
        return path

class Launch(models.Model):
    launch_date = models.DateField()
    notes = models.CharField(max_length=1000)
    members_attending = models.ManyToManyField(
        Account,
        related_name='launches_attended',
    )
    team = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        related_name='launches',
    )

    def __str__(self):
        return self.launch_date.strftime("%B %d, %Y")

    def dashes(self):
        return self.launch_date.strftime("%Y-%m-%d")

class Flight(models.Model):
    launch = models.ForeignKey(
        Launch,
        on_delete=models.CASCADE,
        related_name='flights',
    )
    design = models.ForeignKey(
        Design,
        on_delete=models.CASCADE,
        related_name='flights',
    )
    goal = models.CharField(max_length=500)

    # weather
    temperature = models.IntegerField(null=True)  # Fahrenheit
    wind_speed = models.IntegerField(null=True)  # mph
    weather_notes = models.CharField(max_length=500)

    # descriptions
    rocket_description = models.CharField(max_length=20)
    motor_name = models.CharField(max_length=20)
    motor_delay = models.IntegerField()  # seconds
    parachute_size = models.IntegerField()  # inches
    parachute_description = models.CharField(max_length=20)

    cg_separation_from_cp = models.DecimalField(decimal_places=2, max_digits=8, null=True)  # mm

    # masses in grams
    egg_mass = models.DecimalField(decimal_places=2, max_digits=8)
    wadding_mass = models.DecimalField(decimal_places=2, max_digits=8, null=True)
    ballast_mass = models.DecimalField(decimal_places=2, max_digits=8)
    motor_mass = models.DecimalField(decimal_places=2, max_digits=8, null=True)
    total_mass = models.DecimalField(decimal_places=2, max_digits=8)

    # results
    altitude = models.IntegerField()  # feet
    time = models.DecimalField(decimal_places=2, max_digits=8)  # seconds
    points = models.DecimalField(decimal_places=2, max_digits=8)

    # reflection
    modifications_made = models.CharField(max_length=256)
    damages = models.CharField(max_length=256)
    flight_characteristics = models.CharField(max_length=500)
    considerations_for_next_flight = models.CharField(max_length=256)

    def __str__(self):
        return str(self.launch) + " launch #" + str(list(self.launch.flights.all()).index(self) + 1)

    def flight_num(self):
        return str(list(self.launch.flights.all()).index(self) + 1)
