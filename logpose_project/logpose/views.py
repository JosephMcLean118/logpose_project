from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Count
from logpose.models import Game, Genre, Review
from logpose.forms import UserForm, UserProfileForm, GameSearchForm

# index should return homepage
def index(request):
    """
    Return render of homepage template.
    Context dictionary contains: All games, genres, most_popular_game
    """
    context = {}

    games = Game.objects.all()
    genres = Genre.objects.all()

    if not games.exists():
        return HttpResponse("No Games Found")

    # Find most popular game
    most_popular_game = max(games, key=lambda g: g.avg_rating() or 0)
    context["popular_game"] = most_popular_game

    # Get all genre names as a list then join as string
    genre_names = most_popular_game.genres.values_list('name', flat=True)
    most_popular_game.genre_list = ", ".join(genre_names)

    context["genres"] = genres
    context["games"] = games

    return render(request, 'logpose/home.html', context)



def search_games(request):
    """
    Return filtered render of reviews page template.
    ------------
    NOT COMPLETE
    ------------
    Will complete once reviews page is made
    """
    form = GameSearchForm(request.GET)
    if form.is_valid():
        game_name = form.cleaned_data['game']
        genre = form.cleaned_data['genre']
        stars = form.cleaned_data['stars']
        year = str(form.cleaned_data['year'])
        print(form)
        return HttpResponse(f"Game: {game_name}, Genre: {genre}, Stars: {stars}, Year: {year}"  )
    return HttpResponse("Fail ")

def reviews_for_game(request, slug):
    """
    Return render of reviews page, filtered by games name
    ------------
    NOT COMPLETE
    ------------
    Will complete once reviews page is made
    """
    game = get_object_or_404(Game, slug=slug)
    reviews = game.review_set.all()  # gets all reviews for this game
    return HttpResponse(f"Game: {game.title}, Reviews: {reviews}")




def register(request):
    registered = False

    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST, request.FILES)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'profile_image' in request.FILES:
                profile.profile_image = request.FILES['profile_image']

            profile.save()
            registered = True
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request, 'logpose/register.html', {
        'user_form': user_form,
        'profile_form': profile_form,
        'registered': registered,
    })


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return redirect(reverse('logpose:index'))
            else:
                return render(request, 'logpose/login.html', {
                    'error': 'Your account has been disabled.',
                })
        else:
            return render(request, 'logpose/login.html', {
                'error': 'Invalid username or password.',
            })
    else:
        return render(request, 'logpose/login.html')


@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse('logpose:index'))

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

