from django.shortcuts import render
from logpose.models import Game, Genre
from logpose.forms import GameSearchForm
from django.http import HttpResponse

# Create your views here.

# index should return homepage
def index(request):
    context = {}

    games = Game.objects.all()

    if games.exists():
        most_popular_game = max(games, key=lambda g: g.avg_rating() or 0)
    else:
        # Create some default games if DB is empty
        most_popular_game = Game.objects.create(title="Super Fun Game", release_date="2026-01-01")

    context["popular_game"] = most_popular_game
    context["genres"] = Genre.objects.all()
    context["games"] = games
    return render(request, 'logpose/home.html', context)


def search_games(request):
    form = GameSearchForm(request.GET)
    if form.is_valid():
        game_name = form.cleaned_data['game']
        genre = form.cleaned_data['genre']
        stars = form.cleaned_data['stars']
        print(game_name)
        return HttpResponse(f"Game: {game_name}, Genre: {genre}, Stars: {stars}"  )
    print(form.errors)
    return HttpResponse("Fail ")