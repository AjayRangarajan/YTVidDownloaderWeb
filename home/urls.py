from django.urls import path
from . import views as home_views

app_name = 'home'


urlpatterns = [
    path('', home_views.home, name='home'),
    path('download/', home_views.download, name='download'),
]
