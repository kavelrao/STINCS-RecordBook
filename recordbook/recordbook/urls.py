"""recordbook URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from home import views


# Import sibling folder 'home'
import sys
import os
sys.path.append(os.path.abspath('../home'))
import home


urlpatterns = [
    path('home/', include('home.urls')),
    path('admin/', admin.site.urls),
    path('', home.views.index, name='index'),
    #path('dataEntry/', home.views.dataEntry, name='dataEntry'),
    path('dataEntry/new_launch', home.views.new_launch, name='new_launch'),
    path('dataEntry/log_flight', home.views.log_flight, name='log_flight'),
    path('designs/', home.views.designs, name='designs'),
    path('new_design/', home.views.new_design, name='new_design'),
    path('team/', home.views.team, name='team'),
    path('launches/', home.views.launches, name='launches'),
    path('launch/<str:date>/', home.views.launch, name='launch'),
    path('log_in/', home.views.Login.as_view(template_name='home/log_in.html'), name='log_in'),
    path('log_out/', home.views.log_out, name='log_out'),
    path('homepage/', home.views.homepage, name='homepage'),
    path('register/', home.views.register, name='register'),
    path('register/create_team/', home.views.create_team, name='create_team'),
    path('register/join_team/', home.views.join_team, name='join_team'),
    path('data_analysis/', home.views.data_analysis, name='data_analysis'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
