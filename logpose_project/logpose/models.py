from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify

class Genre(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name
    
class Game(models.Model):
    title = models.CharField(max_length=100, unique=True)
    release_date = models.DateField()
    image = models.ImageField(upload_to="game_images", blank=True)
    slug = models.SlugField(unique=True)
    genres = models.ManyToManyField(Genre)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Game, self).save(*args, **kwargs)

    def avg_rating(self):
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
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    profile_image = models.ImageField(upload_to='profile_images', blank=True)

    def avg_rating_given(self):
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

    def __str__(self):
        return f"{self.user.username} - {self.game.title}"