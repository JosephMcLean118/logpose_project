from django.shortcuts import render, get_object_or_404, redirect
from logpose.models import Game, Genre
from django.http import HttpResponse
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
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

    if games.exists():

        # Find most popular game
        most_popular_game = max(games, key=lambda g: g.avg_rating() or 0)
        context["popular_game"] = most_popular_game

        # Get all genre names as a list then join as string
        genre_names = most_popular_game.genres.values_list('name', flat=True)
        most_popular_game.genre_list = ", ".join(genre_names)

        context["genres"] = genres
        context["games"] = games

        return render(request, 'logpose/home.html', context)
    return HttpResponse("No Games Found")


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

