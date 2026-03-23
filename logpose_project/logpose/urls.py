from django.urls import path
from logpose import views

app_name = 'logpose'

urlpatterns = [
    path('', views.index, name='index'),
    path('reviews/<int:review_id>/', views.review_detail, name='review_detail'),
    path('reviews/create/', views.create_review, name='create_review'),
    path('search/', views.search_games, name='search_games'),
    path('reviews/<slug:slug>/', views.reviews_for_game, name='reviews_for_game'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('reviews/', views.reviews, name='reviews'),
]
