from django.test import TestCase, Client
from django.urls import reverse
from logpose.models import Game, Genre, UserProfile, Review
from populate_logpose import add_genre, add_game, add_user, add_review
from django.contrib.auth.models import User


# ------------Test Authentication and Accounts------------

#----Test the registration feature
class RegistrationTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('logpose:register')

    # Test Registration Page Loads
    def test_register_page_loads(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    # Test valid user can make a profile successfully
    def test_create_valid_user(self):
        response = self.client.post(self.url, {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'password',
            'bio': 'Hello',
        })
        # Check registration was successful
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Account created')

    # Ensure user is added to Users and UserProfiles
    def test_user_is_added_to_users_and_userProfiles(self):
        response = self.client.post(self.url, {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'password',
            'bio': 'Hello',
        })
        self.assertTrue(User.objects.count(), 1)
        self.assertEqual(UserProfile.objects.count(), 1)
        user = User.objects.first()

        # Check that name has been parsed correctly
        self.assertEqual(user.username, 'testuser')

    # Test that userProfile is linked to correct User    
    def test_user_linked_to_userProfile(self):
        self.client.post(self.url, {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'password',
            'bio': 'I am a gamer.',
        })
        user = User.objects.get(username='testuser')
        profile = UserProfile.objects.get(user=user)
        self.assertEqual(profile.bio, 'I am a gamer.')

    # Test no two users with same username can exist
    def test_register_duplicate_username_fails(self):
        User.objects.create_user(username='testuser', password='password')
        self.client.post(self.url, {
            'username': 'testuser',
            'email': 'other@example.com',
            'password': 'password',
        })
        # Still only the original user exists
        self.assertEqual(User.objects.count(), 1)

#----Test the login feature
class LoginTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.url = reverse('logpose:login')
        self.user = User.objects.create_user(
            username='testuser',
            password='password'
        )

    # Test login Page Loads
    def test_login_page_loads(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    # Test valid login is correctly handled
    def test_valid_login_redirect(self):
        response = self.client.post(self.url, {
            'username': 'testuser',
            'password': 'password',
        })

        # Check we are taken back to homepage
        self.assertRedirects(response, reverse('logpose:index'))
    
    # Test valid login is now marked as authenticated
    def test_valid_login_is_authenticated(self):
        self.client.post(self.url, {
            'username': 'testuser',
            'password': 'password',
        })

        # Check user is authenticated
        response = self.client.get(reverse('logpose:index'))
        self.assertTrue(response.wsgi_request.user.is_authenticated)
    
    # Check login with wrong password fails
    def test_login_wrong_password_fails(self):
        response = self.client.post(self.url, {
            'username': 'testuser',
            'password': 'WrongPassword',
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Invalid username or password')
        self.assertFalse(response.wsgi_request.user.is_authenticated)

    # Check login with wrong username fails
    def test_login_wrong_username_fails(self):
        response = self.client.post(self.url, {
            'username': 'WrongUsername',
            'password': 'password',
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Invalid username or password')
        self.assertFalse(response.wsgi_request.user.is_authenticated)
    
    # Check login to nonexistent account fails
    def test_login_to_nonexistent_account_fails(self):
        response = self.client.post(self.url, {
            'username': 'notARealAccount',
            'password': 'password',
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Invalid username or password')
        self.assertFalse(response.wsgi_request.user.is_authenticated)

#----Test the logout button
class LogoutTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('logpose:logout')
        self.user = User.objects.create_user(
            username='testuser',
            password='password'
        )

    # Test logout can only be done for logged in users
    def test_logout_requires_login(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login', response['Location'])
    
    # Test previously authenticated users are no longer authenticated once logged out
    def test_logout_unauthenticates_user(self):
        self.client.login(username='testuser', password='password')
        self.client.get(self.url)
        response = self.client.get(reverse('logpose:index'))
        self.assertFalse(response.wsgi_request.user.is_authenticated)

    # Test upon logging out user is redirected to index
    def test_logout_redirects_to_index(self):
        self.client.login(username='testuser', password='password')
        response = self.client.get(self.url)
        self.assertRedirects(response, reverse('logpose:index'))

#----Test only logged in users can use @login_required features
class LoggedInFeaturesTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='password'
        )
        self.protected_urls = [
            reverse('logpose:create_review'),
            reverse('logpose:logout'),
        ]

    # Check that logged out users are redirected to login when trying to access @login_required features
    def test_unauthenticated_redirected_to_login(self):
        for url in self.protected_urls:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 302,
                             msg=f"Expected redirect at {url}")
            self.assertIn('/login', response['Location'],
                          msg=f"Expected login redirect at {url}")

    # Check that logged in users are are able to access @login_required features
    def test_authenticated_user_not_redirected(self):
        self.client.login(username='testuser', password='password')
        for url in [reverse('logpose:edit_profile'), reverse('logpose:create_review')]:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200,
                             msg=f"Authenticated user should reach {url}")
    
# --------------------------------------------------------


# -------------------Test Game Search---------------------

#----Test the Search Box
class GameSearchTests(TestCase):
    def setUp(self):
        self.client = Client()
        # Add some games and reviews
        # Create one genre
        self.genre = add_genre("RPG")

        # Create one game
        self.game = add_game(
            title="Mario",
            release_date="2020-01-01",
            image="test.jpg"
        )
        self.game.genres.add(self.genre)

        # Create one user
        self.user = add_user(
            username="testuser",
            email="test@test.com",
            password="test123",
            bio="test bio"
        )

        # Create one review
        self.review = add_review(
            user=self.user,
            game=self.game,
            rating=5,
            body="Amazing game"
        )

    # Test that homepage with search box displays
    def test_search_box_displays(self):
        response = self.client.get(reverse('logpose:index'))
        self.assertEqual(response.status_code, 200)

        # check page contains Search Games
        self.assertContains(response, 'Search Games')



    # Test that we can search for game by title
    def test_search_game_appears_for_name(self):
        response = self.client.get(
            reverse('logpose:search_games'),
            {'game': 'Mario'}
        )

        # Follow redirect to /reviews/
        self.assertEqual(response.status_code, 302)
        response = self.client.get(response.url)
        self.assertEqual(response.status_code, 200)

        # Check the game/review appears
        self.assertContains(response, "Mario")
        self.assertContains(response, "Amazing game")

    # Test that we can search for game by Genre
    def test_search_game_appears_for_genre(self):
        response = self.client.get(
            reverse('logpose:search_games'),
            {'genre': 'RPG'}
        )

        self.assertEqual(response.status_code, 302)
        response = self.client.get(response.url)
        self.assertEqual(response.status_code, 200)

        # Check the game/review appears
        self.assertContains(response, "Mario")
        self.assertContains(response, "Amazing game")

    # Test that we can search for game by Release Year
    def test_search_game_appears_for_year(self):
        response = self.client.get(
            reverse('logpose:search_games'),
            {'year': 2020}
        )

        self.assertEqual(response.status_code, 302)
        response = self.client.get(response.url)
        self.assertEqual(response.status_code, 200)

        # Check the game/review appears
        self.assertContains(response, "Mario")
        self.assertContains(response, "Amazing game")

    # Test that we can search for game by Stars
    def test_search_game_appears_for_rating(self):
        response = self.client.get(
            reverse('logpose:search_games'),
            {'rating': 5}
        )

        self.assertEqual(response.status_code, 302)
        response = self.client.get(response.url)
        self.assertEqual(response.status_code, 200)

        # Check the game/review appears
        self.assertContains(response, "Mario")
        self.assertContains(response, "Amazing game")

    # Test searching for a game that doesnt exist in all ways (title, genre, year)
    def test_search_for_game_title_that_doesnt_exist(self):
        response = self.client.get(reverse('logpose:reviews') + "?search=RandomGame")
        self.assertEqual(response.status_code, 200)
        self.assertQuerySetEqual(response.context['reviews'], [])
    
    def test_search_for_game_genre_that_doesnt_exist(self):
        response = self.client.get(reverse('logpose:reviews'), {'genre':"rock"})
        self.assertEqual(response.status_code, 200)
        self.assertQuerySetEqual(response.context['reviews'], [])

    def test_search_for_game_year_that_doesnt_exist(self):
        response = self.client.get(reverse('logpose:reviews'),{'year':1978})
        self.assertEqual(response.status_code, 200)
        self.assertQuerySetEqual(response.context['reviews'], [])

    # Test searching for a game with multiple filters - THAT EXISTS
    def test_search_for_game_year_and_name_that_exists(self):
        response = self.client.get(reverse('logpose:search_games'),{'game': 'Mario', 'year': 2020})
        self.assertEqual(response.status_code, 302)
        response = self.client.get(response.url)
        self.assertEqual(response.status_code, 200)

        # Check the game/review appears
        self.assertContains(response, "Mario")
        self.assertContains(response, "Amazing game")

    # Test searching for a game with multiple filters - THAT DOES NOT EXIST
    def test_search_for_game_year_and_name_that_does_not_exist(self):
        response = self.client.get(reverse('logpose:reviews'),{'game':'Mario', 'year':1978})
        self.assertEqual(response.status_code, 200)
        self.assertQuerySetEqual(response.context['reviews'], [])

    # Test that we get all games if user fills out nothing in the form
    def test_search_empty(self):
        response = self.client.get(reverse('logpose:reviews'),{})
        self.assertEqual(response.status_code, 200)

        # Check the game/review appears

        # We should see mario since it shows all games if nothing is passed in
        self.assertContains(response, "Mario")
        self.assertContains(response, "Amazing game")

# --------------------------------------------------------

# --------Test Most Popular Game and Game Ranking---------
class GameRankingTests(TestCase):
    def setUp(self):
        # Add some games and reviews

        # Two games needed, just need to ensure website knows which is better than the other
        # Create one genre
        self.genre = add_genre("RPG")

        # Create one game
        self.game1 = add_game(
            title="Fortnite",
            release_date="2022-01-01",
            image="test.jpg"
        )
        self.game1.genres.add(self.genre)

        # Create another game
        self.game2 = add_game(
            title="Mario",
            release_date="2020-01-01",
            image="test.jpg"
        )
        self.game2.genres.add(self.genre)

        # Create one user
        self.user = add_user(
            username="testuser",
            email="test@test.com",
            password="test123",
            bio="test bio"
        )

        # Create first review
        self.review2 = add_review(
            user=self.user,
            game=self.game2,
            rating=5,
            body="Amazing game"
        )

        # Create other review
        self.review1 = add_review(
            user=self.user,
            game=self.game1,
            rating=1,
            body="Rubbish game"
        )

    # Check that most popular game is displayed on homepage
    def test_most_popular_game(self):
        response = self.client.get(reverse('logpose:index'))
        # Page should contain mario since it would be the most popular game
        top_game = response.context['popular_game']
        self.assertEqual(top_game.title, "Mario")

    # Check read reviews button for most popular game works
    def test_read_review_popular_works(self):
        review_detail_url = reverse('logpose:review_detail', kwargs={'review_id': self.review2.id})

        detail_response = self.client.get(review_detail_url)
        self.assertEqual(detail_response.status_code, 200)

        self.assertContains(detail_response, "Mario")
        self.assertContains(detail_response, self.user.username)
        self.assertContains(detail_response, "Amazing game")
        self.assertContains(detail_response, "5")  # rating

    # Test that ranking works correctly (mario should be first)
    def test_game_ranking(self):
        response = self.client.get(reverse('logpose:reviews'))
        top_games = list(response.context['top_games'])
        self.assertEqual(top_games[0].title, "Mario")

    def test_game_ranking_displays(self):
        response = self.client.get(reverse('logpose:reviews'))
        # Title is apart of same card so we can check title to see if ranking is displayed
        self.assertContains(response, "Top 10 Games")

# --------------------------------------------------------

# -------------------Test Create Review-------------------
class CreateReviewTests(TestCase):
    def setUp(self):
        # Create one user, one game and log the user in otherwise they cannot review
        self.user = add_user(
            username="testuser",
            email="test@test.com",
            password="test123",
            bio="test bio"
        )
        self.genre = add_genre("RPG")

        # Create one game
        self.game = add_game(
            title="Fortnite",
            release_date="2022-01-01",
            image="test.jpg"
        )
        self.game.genres.add(self.genre)

        self.client.post(reverse("logpose:login"), {
            'username': 'testuser',
            'password': 'test123',
        })

    # Check the create_review widget displays correctly
    def test_create_review_displays(self):
        response = self.client.get(reverse('logpose:create_review'))
        self.assertTemplateUsed(response, 'logpose/create_review.html')
        self.assertContains(response, "Write a Review")
        self.assertContains(response, "Game")
        self.assertContains(response, "Rating")
        self.assertContains(response, "Body")
        self.assertContains(response, "Submit Review")

    # Check that we can create a review
    def test_review_can_be_made(self):
        response = self.client.post(reverse('logpose:create_review'), {
            'game': self.game.id,
            'rating': 5,
            'body': "This game is awesome!"
        }) 
        self.assertEqual(response.status_code, 302)

        # Check that review has been added to db
        review = Review.objects.filter(user=self.user, game=self.game).first()
        self.assertIsNotNone(review)
        self.assertEqual(review.rating, 5)
        self.assertEqual(review.body, "This game is awesome!")

    def test_review_for_no_game(self):
        response = self.client.post(reverse('logpose:create_review'), {
            'game': "",
            'rating': 5,
            'body': "This game is awesome!"
        })

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Write a Review")  # form is shown again
         # Check that review has NOT been added to db
        self.assertEqual(Review.objects.count(), 0) 

# --------------------------------------------------------

# -----------------Test Indiviudal Reviews----------------
class IndividualReviewTests(TestCase):
    # Create a user that has reviewed one game
    def setUp(self):
        # One games needed
        # Create one genre
        self.genre = add_genre("RPG")

        # Create one game
        self.game1 = add_game(
            title="Fortnite",
            release_date="2022-01-01",
            image="test.jpg"
        )
        self.game1.genres.add(self.genre)
        # Create one user
        self.user = add_user(
            username="testuser",
            email="test@test.com",
            password="test123",
            bio="test bio"
        )

        self.client.post(reverse("logpose:login"), {
            'username': 'testuser',
            'password': 'test123',
        })

        # Create first review
        self.review = add_review(
            user=self.user,
            game=self.game1,
            rating=5,
            body="Amazing game"
        )
    def test_read_full_review_works(self):
        review_detail_url = reverse('logpose:review_detail', kwargs={'review_id': self.review.id})

        # Simulate clicking the link
        detail_response = self.client.get(review_detail_url)
        self.assertEqual(detail_response.status_code, 200)
        self.assertTemplateUsed(detail_response, 'logpose/review_detail.html')
        

        # Assert full review content appears
        self.assertContains(detail_response, self.game1.title)
        self.assertContains(detail_response, self.user.username)
        self.assertContains(detail_response, "Amazing game")
        self.assertContains(detail_response, "5")  

# --------------------------------------------------------

# -----------------Test Profile Page----------------------

class ProfilePageTest(TestCase):
    def setUp(self):
        # Create logged in user
        self.user = add_user(
            username="testuser",
            email="test@test.com",
            password="test123",
            bio="test bio"
        )
        self.client.login(username='testuser', password='test123')

    # Check I can get to profile page from button
    def test_profile_button_works(self):
        # Build profile URL
        profile_url = reverse('logpose:profile', kwargs={'username': self.user.username})

        # Simulate clicking the "Profile" button
        response = self.client.get(profile_url)

        # Check status code
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'logpose/profile.html')

    # Check profile details are displayed
    
    def test_profile_details_are_displayed(self):
        # Build profile URL
        profile_url = reverse('logpose:profile', kwargs={'username': self.user.username})
        

        # Simulate clicking the "Profile" button
        response = self.client.get(profile_url)
        self.assertContains(response, self.user.username)
        self.assertContains(response, self.user.userprofile.bio)

    # Check edit profile button takes user to new page
    def test_edit_profile_button_works(self):
        # Build profile URL
        profile_url = reverse('logpose:profile', kwargs={'username': self.user.username})
        response = self.client.get(profile_url)
        self.assertEqual(response.status_code, 200)
        
    def test_edit_profile_displays(self):
        # Build profile URL
        edit_url = reverse('logpose:edit_profile')
        response = self.client.get(edit_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Edit Profile")

    # Check edit profile works
    def test_edit_profile_works(self):
        edit_url = reverse('logpose:edit_profile')
        new_bio = "This is my updated bio"
        response = self.client.post(edit_url, {'bio': new_bio})

        # After editing, we should redirect to the profile page
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('logpose:profile', kwargs={'username': self.user.username}), response.url)

        # Fetch the user profile from the database
        self.user.userprofile.refresh_from_db()

        # Assert that the bio was updated
        self.assertEqual(self.user.userprofile.bio, new_bio)

