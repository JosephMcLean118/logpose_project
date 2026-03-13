import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'logpose_project.settings')

import django
django.setup()

from logpose.models import Genre, Game, User, UserProfile, Review
from datetime import datetime
import csv

def populate():
    """
    Populates the Logpose database with:
    - 10 genres
    - 30 games (from CSV)
    - 5 test users with profiles
    - 10 sample reviews """
    
    print("Starting population script...")

    # Clear old data
    Genre.objects.all().delete()
    Game.objects.all().delete()
    User.objects.all().delete()
    UserProfile.objects.all().delete()
    Review.objects.all().delete()

    
    # Creating genres
    # Dictionary to store genre objects for later use
    genres = {}
    genres_list = ['Action', 'Adventure', 'RPG', 'Horror', 'MMO', 
                   'Strategy', 'Sports', 'Simulation', 'Shooter', 'Survival']
    
    # Loop through each genre name and create Genre objects
    for genre_name in genres_list:
        g = add_genre(genre_name)
        genres[genre_name] = g # Store genre object in dictionary for later use
    
    # CREATE GAMES FROM CSV
    # Open CSV file and read game data
    with open('Games.csv', 'r', encoding='utf-8') as file:
        # DictReader treats first row as column names
        reader = csv.DictReader(file)
        
        # Loop through each row in CSV (each game)
        for row in reader:
            # Create game object with title, release date, and image
            game = add_game(
                title=row['Title'],
                release_date=row['Release Date'],
                image=row['Image']
            )
            game.save()
            game = Game.objects.get(pk=game.pk)

            # Add genres to game (ManyToMany relationship)
            # Checks if Genre1,2,3 exists and are not empty
            if row.get('Genre1') and row['Genre1'].strip():
                game.genres.add(genres[row['Genre1'].strip()])
            
            if row.get('Genre2') and row['Genre2'].strip():
                game.genres.add(genres[row['Genre2'].strip()])
            
            if row.get('Genre3') and row['Genre3'].strip():
                game.genres.add(genres[row['Genre3'].strip()])

# Create EXAMPLE USERS 
# dictkey : usrname, email, password, bio
    users = {
        'dennis': add_user('dennis', 'dennis@gmail.com', 'testing123', 
                          'Busy businessman looking for the best games. No time to waste - just want top-rated titles!'),
        'peter': add_user('peter', 'peter@gmail.com', 'testing123', 
                         'Aspiring game streamer and reviewer. Building my reputation one review at a time!'),
        'christy': add_user('christy', 'christy@gmail.com', 'testing123', 
                           'Looking for great games to gift my gamer boyfriend. Always reading reviews first!'),
        'alice': add_user('alice', 'alice@gmail.com', 'testing123', 
                         'Love RPGs and adventure games! Always looking for the next epic story.'),
        'bob': add_user('bob', 'bob@gmail.com', 'testing123', 
                       'Action game enthusiast. If it has explosions, Im in!'),
    }

    # Retrieve all games for review creation
    all_games = list(Game.objects.all())
    
    # Create EXAMPLE REVIEWS
    # Dennis busy guy
    add_review(users['dennis'], all_games[0], 5, 'Excellent. Worth the price. Highly recommend.')
    
    # Peter aspiring reviewer
    add_review(users['peter'], all_games[1], 5, 'Absolutely a masterpiece! Best game I\'ve played in years.')
    add_review(users['peter'], all_games[2], 4, 'Great RPG with deep mechanics. Totally worth it for serious gamers.')
    add_review(users['peter'], all_games[26], 2, 'Disappointing. The gameplay feels rushed and unfinished. Not worth the hype.')
    
    # Christy buying for boyfriend
    add_review(users['christy'], all_games[3], 5, 'Bought this for my boyfriend and he loves it! We play together now.')
    add_review(users['christy'], all_games[29], 1, 'Bought this for my boyfriend last year and he was so disappointed. Terrible game. Never again!')
    
    # Alice RPG enthusiast
    add_review(users['alice'], all_games[1], 4, 'Beautiful adventure with amazing storytelling.')
    add_review(users['alice'], all_games[28], 2, 'Expected more from this RPG. Story was weak and combat felt clunky.')
    
    # Bob action fan 
    add_review(users['bob'], all_games[0], 4, 'Solid action game with great combat.')
    add_review(users['bob'], all_games[4], 5, 'Non-stop action from start to finish!')
    
    print(f"Genres: {Genre.objects.count()}")
    print(f"Games: {Game.objects.count()}")
    print(f"Users: {User.objects.count()}")
    print(f"Reviews: {Review.objects.count()}")

def add_genre(name):
    """
    Creates or retrieves a Genre object.
    get_or_create returns (object, created_boolean), [0] gets just the object
    """
    g = Genre.objects.get_or_create(name=name)[0]
    g.save()
    return g

def add_game(title, release_date, image):
    """
    Creates or retrieves a Game object.
    Uses defaults to set required fields during creation.
    """
    g, created = Game.objects.get_or_create(
        title=title,
        defaults={
            'release_date': release_date,
            'image': f"game_images/{image}"
        }
    )
    
    # If game already existed, update its fields 
    # this allows us to run the script multiple times without creating duplicates, but still update existing entries if needed
    if not created:
        g.release_date = release_date
        g.image = f"game_images/{image}"
        g.save()
    
    return g

def add_user(username, email, password, bio):
    """
    Creates a User and UserProfile.
    Password is hashed for security.
    """
    # Create User
    user = User.objects.get_or_create(username=username, email=email)[0]
    user.set_password(password) # Hashes the password using Django's built-in method
    user.save()
    
    # Create UserProfile linked to User
    profile = UserProfile.objects.get_or_create(user=user)[0]
    profile.bio = bio
    profile.save()
    
    return user

def add_review(user, game, rating, body):
    """
    Creates or retrieves a Review.
    Links user to game with rating and text.
    """
    r, created = Review.objects.get_or_create(
        user=user,
        game=game,
        defaults={
            'rating': rating,
            'body': body
        }
    )
    
    # If review already existed, update its fields
    # # this allows us to run the script multiple times without creating duplicates, but still update existing entries if needed
    if not created:
        r.rating = rating
        r.body = body
        r.save()

    return r


if __name__ == '__main__':
    print('Starting Logpose population script...')
    populate()
    print('Population complete!')