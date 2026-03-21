from django.urls import path
from logpose import views

app_name = 'logpose'

urlpatterns = [
    path('reviews/', views.reviews, name='reviews'),
]
