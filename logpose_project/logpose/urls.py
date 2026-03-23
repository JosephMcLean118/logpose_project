 #kai-----------------------------
from django.contrib import admin
from django.urls import path
from . import views

app_name = 'logpose'

urlpatterns = [
    path('', views.index, name='index'),

   
    path('admin/', admin.site.urls),
    path('edit/', views.edit_profile, name='edit_profile'),
    path('user/<str:username>/', views.profile_view, name='profile'),
    #-----------------------------
]
