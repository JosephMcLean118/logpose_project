from django.urls import path
from logpose import views

app_name = 'logpose'

urlpatterns = [
    path('', views.index, name='index'),
]
