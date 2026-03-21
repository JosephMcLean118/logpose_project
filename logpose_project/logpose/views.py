from django.shortcuts import render
from django.db.models import Avg, Count
from logpose.models import Game, Genre, Review


def index(request):
    return render(request, 'logpose/base.html')

def reviews(request):
    """
    Displays all reviews with filtering options.
    Filters: genre, rating, year, search (game name)
    """
    # Start with all reviews
    reviews = Review.objects.all().select_related('user', 'game').order_by('-created_at')
    
    # Get all genres for tabs
    genres = Genre.objects.all()
    
    # Filters by GENRE
    genre_filter = request.GET.get('genre')
    if genre_filter:
        reviews = reviews.filter(game__genres__name=genre_filter)
    
    # Filters by RATING
    rating_filter = request.GET.get('rating')
    if rating_filter:
        reviews = reviews.filter(rating=rating_filter)
    
    # Filters by YEAR
    year_filter = request.GET.get('year')
    if year_filter:
        reviews = reviews.filter(game__release_date__year=year_filter)
    
    # Search by GAME NAME
    search_query = request.GET.get('search')
    if search_query:
        reviews = reviews.filter(game__title__icontains=search_query)
    
    # TOP 5 GAMES by average rating (only games with reviews)
    top_games = Game.objects.annotate(
        avg_rating=Avg('review__rating'),
        review_count=Count('review')
    ).filter(review_count__gt=0).order_by('-avg_rating')[:5]
    
    context = {
        'reviews': reviews,
        'genres': genres,
        'top_games': top_games,
        'current_genre': genre_filter,
        'current_rating': rating_filter,
        'current_year': year_filter,
        'current_search': search_query,
    }
    
    return render(request, 'logpose/reviews.html', context)
