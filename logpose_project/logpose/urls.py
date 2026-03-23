from django.urls import path
from logpose import views

app_name = 'logpose'

urlpatterns = [
    path('', views.index, name='index'),
    path('reviews/<int:review_id>/', views.review_detail, name='review_detail'),
    path('reviews/create/', views.create_review, name='create_review'),
]
