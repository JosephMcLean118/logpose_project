from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify

class Genre(models.Model):
    # Stores game genres
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name
    
class Game(models.Model):
    title = models.CharField(max_length=100, unique=True)
    release_date = models.DateField()
    image = models.ImageField(upload_to="game_images", blank=True)
    # Slug is auto generated from title for use in urls
    slug = models.SlugField(unique=True)
    # A game can belong to multiple genres and a genre can have multiple games
    genres = models.ManyToManyField(Genre)

    def save(self, *args, **kwargs):
        # auto generates slug from title
        self.slug = slugify(self.title)
        super(Game, self).save(*args, **kwargs)

    def avg_rating(self):
        """
        calculates the average rating from all reviews of that game
        """
        reviews = self.review_set.all()
        if reviews:
            total = sum([review.rating for review in reviews])
            return round(total / len(reviews), 1)
        return None
    
    def num_reviews(self):
        return self.review_set.count()

    def __str__(self):
        return self.title
    
class UserProfile(models.Model):
    """
    Extends Djangos built in user model with additional profile fields.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE) # each user only has 1 profile
    bio = models.TextField(blank=True)
    profile_image = models.ImageField(upload_to='profile_images', blank=True)

    def avg_rating_given(self):
        """
        calculates the average star rating
        """
        reviews = self.user.review_set.all()
        if reviews:
            total = sum([review.rating for review in reviews])
            return round(total / len(reviews), 1)
        return None
    
    def __str__(self):
        return self.user.username
    

class Review(models.Model):
    RATING_CHOICES = [(i, i) for i in range(1, 6)]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=RATING_CHOICES)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        # Ensures a user can only review each game once
        unique_together = ('user', 'game')

    def __str__(self):
        return f"{self.user.username} - {self.game.title}"