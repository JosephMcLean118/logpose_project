from django.contrib import admin
from logpose.models import Genre, Game, UserProfile, Review

# Register your models here.
admin.site.register(Genre)
admin.site.register(Game)
admin.site.register(UserProfile)
admin.site.register(Review)