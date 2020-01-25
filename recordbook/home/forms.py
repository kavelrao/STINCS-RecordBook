from .models import User, Team

from django import forms
from django.contrib.auth.hashers import check_password

class CreateTeamForm(forms.Form):
    team_name = forms.CharField(max_length=50)
    captain_first_name = forms.CharField(max_length=256)
    captain_last_name = forms.CharField(max_length=256)
    captain_email = forms.EmailField(max_length=256)
    captain_username = forms.CharField(max_length=256)
    captain_password = forms.CharField(max_length=256, widget=forms.PasswordInput)

    def clean_team_name(self):
        name = self.cleaned_data['team_name']
        for team in Team.objects.all():
            if name == team.name:
                raise forms.ValidationError('Team name already in use')
                break
        return name

    def clean_captain_email(self):
        email = self.cleaned_data['captain_email']
        for user in User.objects.all():
            if email == user.email:
                raise forms.ValidationError('An account with that email already exists')
                break
        return email

    def clean_captain_username(self):
        username = self.cleaned_data['captain_username']
        for user in User.objects.all():
            if username == user.username:
                raise forms.ValidationError('An account with that username already exists')
                break
        return username

class JoinTeamForm(forms.Form):
    team_join_code = forms.CharField(max_length=8)
    first_name = forms.CharField(max_length=256)
    last_name = forms.CharField(max_length=256)
    email = forms.EmailField(max_length=256)
    username = forms.CharField(max_length=256)
    password = forms.CharField(max_length=256, widget=forms.PasswordInput)

    def clean_email(self):
        email = self.cleaned_data['email']
        for user in User.objects.all():
            if email == user.email:
                raise forms.ValidationError('An account with that email already exists')
                break
        return email

    def clean_username(self):
        username = self.cleaned_data['username']
        for user in User.objects.all():
            if username == user.username:
                raise forms.ValidationError('An account with that username already exists')
                break
        return username

class DesignForm(forms.Form):
    name = forms.CharField(max_length=256)
    motor_diameter = forms.IntegerField(label='Motor diameter (mm)') # millimeters
    fin_description = forms.CharField(max_length=500)
    length = forms.DecimalField(label='Rocket length (mm)')  # millimeters
    diameter = forms.DecimalField(label='Rocket diameter (mm)')  # millimeters


class LaunchEntryForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(LaunchEntryForm, self).__init__(*args, **kwargs)
        members = self.user.account.team.accounts.all()
        for i in range(len(members)):
            field_name = 'member_%s' % (members[i].user.username,)
            field_label = "Did " + members[i].user.first_name + " attend?"
            self.fields[field_name] = forms.BooleanField(required=False, label=field_label)

    def get_member_fields(self):
        fields = []
        for field in self.fields:
            if field.startswith('member_'):
                fields.append(field)
        return fields

    def get_non_member_fields(self):
        fields = []
        for field in self.fields:
            if not field.startswith('member_'):
                fields.append(field)
        return fields

    launch_date = forms.DateField()
    notes = forms.CharField(max_length=1000)


# Helper function for FlightEntryForm
def get_team_launch_dates(user):
    dates = []
    for launch in user.account.team.launches:
        dates.append((str(launch.launch_date), launch.launch_date.strftime("%B %d, %Y")))
    return dates

class FlightEntryForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(FlightEntryForm, self).__init__(*args, **kwargs)
        self.fields['launch'] = forms.ChoiceField(choices=get_team_launch_dates(self.user))

    goal = forms.CharField(max_length=500)

    # weather
    temperature = forms.IntegerField()  # Fahrenheit
    wind_speed = forms.IntegerField()  # mph
    weather_notes = forms.CharField(max_length=500)

    # descriptions
    payload_description = forms.CharField(max_length=20)
    booster_description = forms.CharField(max_length=20)
    motor_name = forms.CharField(max_length=20)
    motor_delay = forms.IntegerField()  # seconds
    parachute_size = forms.IntegerField()  # inches
    parachute_description = forms.CharField(max_length=20, required=False)

    cg_separation_from_cp = forms.DecimalField()  # inches

    # masses in grams
    egg_mass = forms.DecimalField()
    wadding_mass = forms.DecimalField()
    ballast_mass = forms.DecimalField()
    motor_mass = forms.DecimalField()
    total_mass = forms.DecimalField()

    # results
    altitude = forms.IntegerField()  # feet
    time = forms.DecimalField()  # seconds

    # reflection
    modifications_made = forms.CharField(max_length=256)
    damages = forms.CharField(max_length=256)
    flight_characteristics = forms.CharField(max_length=500)
    considerations_for_next_flight = forms.CharField(max_length=256)
    log_another_flight = forms.BooleanField(required=False, label='Would you like to log another flight?')



# Not used
class LoginForm(forms.Form):
    username = forms.CharField(max_length=256)
    password = forms.CharField(max_length=256, widget=forms.PasswordInput)

    def clean(self):
        form_data = self.cleaned_data
        user = User.objects.get(username=form_data['username'])
        if user == None:
            self._errors = ['Username and password do not match']
        else:
            if not check_password(form_data['password'], user.password): # If the given password doesn't mach user's hashed password
                self._errors = ['Username and password do not match']
                del form_data['password']
        return form_data
