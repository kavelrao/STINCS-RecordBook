from .forms import CreateTeamForm, JoinTeamForm, DesignForm, LaunchEntryForm, FlightEntryForm
from .models import User, Account, Team, Design, Flight, Launch

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required

import datetime
import random

def index(request):
    context = {}
    return render(request, 'home/index.html', context)

class Login(LoginView):
    template_name = 'home/log_in.html'
    authentication_form = AuthenticationForm
    redirect_field_name = 'homepage'
    redirect_authenticated_user = True

def log_out(request):
    logout(request)
    return redirect('index')

def register(request):
    context = {'create_team': '/register/create_team/', 'join_team': '/register/join_team/'}
    return render(request, 'home/register.html', context)

def create_team(request):
    if request.method == "POST":
        form = CreateTeamForm(request.POST)
        if form.is_valid():
            # Get attributes from the form
            team_name = form.cleaned_data['team_name']
            captain_username = form.cleaned_data['captain_username']
            captain_password = form.cleaned_data['captain_password']
            captain_email = form.cleaned_data['captain_email']
            captain_first_name = form.cleaned_data['captain_first_name']
            captain_last_name = form.cleaned_data['captain_last_name']
            join_code = generate_join_code()
            # Create the new team
            team = Team(name=team_name, join_code=join_code)
            team.save()
            # Create a new user and add attributes
            captain_user = User.objects.create_user(username=captain_username, password=captain_password)
            captain_user.email = captain_email
            captain_user.first_name = captain_first_name
            captain_user.last_name = captain_last_name
            captain_user.save()
            # Create a new account associated with the user
            captain = Account(user=captain_user, team=team, is_captain=True)
            captain.save()
            # Log in user and display the join code
            login(request, captain_user)
            context = {'success': True, 'form': form, 'join_code': join_code}
            return render(request, 'home/create_team.html', context)
        # If form is invalid
        context = {'success': False, 'form': form}
        return render(request, 'home/create_team.html', context)

    else:
        form = CreateTeamForm()
        context = {'success': False, 'form': form}
        return render(request, 'home/create_team.html', context)

def join_team(request):
    if request.method == "POST":
        form = JoinTeamForm(request.POST)
        if form.is_valid():
            # Get attributes from the form
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            join_code = form.cleaned_data['team_join_code']
            # Create a new user and add attributes
            user = User.objects.create_user(username=username, password=password)
            user.email = email
            user.first_name = first_name
            user.last_name = last_name
            user.save()
            print(user)
            # Find the Team associated with the join code
            team = Team.objects.get(join_code=join_code)
            # Create a new account associated with the user
            account = Account(user=user, team=team, is_captain=False)
            account.save()

            # Log in user and redirect to homepage
            login(request, user)
            return redirect('homepage')
        # If form is invalid
        context = {'form': form}
        return render(request, 'home/join_team.html', context)

    else:
        form = JoinTeamForm()
        context = {'form': form}
        context['form'] = form
        return render(request, 'home/join_team.html', context)

@login_required
def homepage(request):
    context = {}
    return render(request, 'home/homepage.html', context)

@login_required
def designs(request):
    context = set_context(request)
    return render(request, 'home/designs.html', context)

@login_required
def new_design(request):
    if request.method == "POST":
        form = DesignForm(request.POST, user=request.user)
        if form.is_valid():
            # Get attributes from the form
            name = form.cleaned_data['name']
            motor_diameter = form.cleaned_data['motor_diameter']
            fin_description = form.cleaned_data['fin_description']
            length = form.cleaned_data['length']
            diameter = form.cleaned_data['diameter']
            # Create a new design and add attributes
            design = Design(name=name, motor_diameter=motor_diameter,
                fin_description=fin_description, length=length, diameter=diameter,
                owner=request.user.account, team=request.user.account.team)
            design.save()

            # Redirect to designs
            return redirect('designs')
        # If form is invalid
        context = {'form': form}
        return render(request, 'home/new_design.html', context)

    else:
        form = DesignForm(user=request.user)
        context = {'form': form}
        return render(request, 'home/new_design.html', context)

@login_required
def team(request):
    context = set_context(request)
    return render(request, 'home/team.html', context)

"""
@login_required
def dataEntry(request):
    context = {}
    return render(request, 'home/dataEntry.html', context)
"""

# Helper functions for new_launch to convert field names into Field objects
def generate_member_fields(form):
    list = []
    for field in form.get_member_fields():
        list.append(form[field])
    return list
def generate_non_member_fields(form):
    list = []
    for field in form.get_non_member_fields():
        list.append(form[field])
    return list

@login_required
def new_launch(request):
    if request.method == "POST":
        form = LaunchEntryForm(request.POST, user=request.user)
        if form.is_valid():
            # Get attributes from the form
            launch_date = form.cleaned_data['launch_date']
            notes = form.cleaned_data['notes']

            # Create a new launch and add attributes
            launch = Launch(launch_date=launch_date, notes=notes, team=request.user.account.team)
            launch.save()

            # Add members to attendance
            for field in form.get_member_fields():
                if form.cleaned_data[field]:
                    username = field[7:]
                    member_account = Account.objects.get(user__username=username)
                    launch.members_attending.add(member_account)

            # Redirect to designs
            return redirect('launches')
        # If form is invalid
        context = {'form': form, 'member_fields': generate_member_fields(form), 'non_member_fields': generate_non_member_fields(form)}
        return render(request, 'home/new_launch.html', context)

    else:
        form = LaunchEntryForm(user=request.user)

        context = {'form': form, 'member_fields': generate_member_fields(form), 'non_member_fields': generate_non_member_fields(form)}
        return render(request, 'home/new_launch.html', context)

@login_required
def log_flight(request):
    if request.method == "POST":
        form = FlightEntryForm(request.POST, user=request.user)
        if form.is_valid():
            # Get attributes from the form
            launch = Launch.objects.get(launch_date=form.cleaned_data['launch'], team=request.user.account.team)
            goal = form.cleaned_data['goal']
            temperature = form.cleaned_data['temperature']
            wind_speed = form.cleaned_data['wind_speed']
            weather_notes = form.cleaned_data['weather_notes']
            rocket_description = form.cleaned_data['rocket_description']
            motor_name = form.cleaned_data['motor_name']
            motor_delay = form.cleaned_data['motor_delay']
            parachute_size = form.cleaned_data['parachute_size']
            parachute_description = form.cleaned_data['parachute_description']
            cg = form.cleaned_data['cg_separation_from_cp']
            egg_mass = form.cleaned_data['egg_mass']
            wadding_mass = form.cleaned_data['wadding_mass']
            ballast_mass = form.cleaned_data['ballast_mass']
            motor_mass = form.cleaned_data['motor_mass']
            total_mass = form.cleaned_data['total_mass']
            altitude = form.cleaned_data['altitude']
            time = form.cleaned_data['time']
            mods = form.cleaned_data['modifications_made']
            damages = form.cleaned_data['damages']
            flight_characteristics = form.cleaned_data['flight_characteristics']
            considerations_for_next_flight = form.cleaned_data['considerations_for_next_flight']
            # The Design field is only there if there are 2+ to choose from
            if len(request.user.account.team.designs.all()) > 1:
                design = Design.objects.get(name=form.cleaned_data['design'], team=request.user.account.team)
            else:
                design = Design.objects.get(team=request.user.account.team)

            # Calculating point value
            if time < 41:
                time_off = 41.0 - time
            elif time > 43:
                time_off = time - 43.0
            else:
                time_off = 0.0
            points = abs(800.0 - altitude) + (4 * time_off)

            # Create a new Flight and add attributes
            flight = Flight(
                launch=launch, design=design, goal=goal, temperature=temperature, wind_speed=wind_speed,
                weather_notes=weather_notes, rocket_description=rocket_description,
                motor_name=motor_name, motor_delay=motor_delay, parachute_size=parachute_size,
                parachute_description=parachute_description, cg_separation_from_cp=cg,
                egg_mass=egg_mass, wadding_mass=wadding_mass, ballast_mass=ballast_mass,
                motor_mass=motor_mass, total_mass=total_mass, altitude=altitude,
                time=time, poitns=points, modifications_made=mods, damages=damages,
                flight_characteristics=flight_characteristics,
                considerations_for_next_flight=considerations_for_next_flight)
            flight.save()

            # If they would like to log another flight, redirect to same page
            if form.cleaned_data['log_another_flight']:
                return redirect('log_flight')

            # Redirect to launch page otherwise
            date = form.cleaned_data['launch'].dashes()
            return redirect('/launches/' + date)

        # If form is invalid
        context = {'form': form}
        return render(request, 'home/log_flight.html', context)

    else:
        form = FlightEntryForm(user=request.user)
        order = ['launch']
        # The Design field is only there if there are 2+ to choose from
        if len(request.user.account.team.designs.all()) > 1:
            order.append('designs')
        form.order_fields(order)
        context = {'form': form}
        return render(request, 'home/log_flight.html', context)


@login_required
def launches(request):
    context = {'launches': request.user.account.team.launches.all()}
    return render(request, 'home/launches.html', context)


@login_required
def launch(request, date):
    ymd = date.split('-')
    date_obj = datetime.date(year=int(ymd[0]), month=int(ymd[1]), day=int(ymd[2]))
    # Redirect user if the launch doesn't exist
    if len(Launch.objects.filter(team=request.user.account.team, launch_date=date_obj)) == 0:
        return redirect('launches')
    launch = Launch.objects.get(team=request.user.account.team, launch_date=date_obj)
    context = {'launch': launch}
    return render(request, 'home/launch.html', context)

def generate_join_code():
    join_code = ''
    for i in range(8):
        join_code = join_code + str(random.randint(0,9))
    unique = True
    for team in Team.objects.all():
        if join_code == team.join_code:
            unique = False
            break
    if unique:
        return join_code
    else:
        return generate_join_code()

def set_context(request):
    user = request.user
    account = user.account
    team = account.team
    captain = team.accounts.get(is_captain=True)
    designs = []
    for account in team.accounts.all():
        for design in account.designs.all():
            designs.append(design)
    context = {
    'request': request,
    'user': user,
    'team': team,
    'account': account,
    'captain': captain,
    'designs': designs
    }
    return context
