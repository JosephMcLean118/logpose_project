from django.shortcuts import render, get_object_or_404
from logpose.models import Game, Genre
from logpose.forms import GameSearchForm
from django.http import HttpResponse

# Create your views here.

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
        year = str(form.cleaned_data['year'])[:-6]
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