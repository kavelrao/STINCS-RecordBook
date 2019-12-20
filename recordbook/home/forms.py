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
