# logpose
Web app project for WAD2

## Overview
Logpose is a game review platform powered by Django. Anyone can browse, search, and filter game reviews, but logged-in users can contribute to the community by writing reviews, rating games (1–5 stars), and customising their profile.

The app is designed to help gamers discover new titles, read honest community reviews, and keep track of the most popular and highest-rated games — all in one place.

## 🛠️ Tech Stack

### Backend
- **Django 6.0.2** - Python web framework
- **Python 3.12** - Programming language
- **SQLite** - Database (development)

### Frontend
- **Bootstrap 5.3.3** - Responsive CSS framework
- **Bootstrap Icons 1.11.3** - Icon library
- **HTML & CSS** - Markup and styling
- **JavaScript** - Client-side interactivity

### Additional Libraries
- **Pillow 12.1.1** - Python image processing library

## 📦 Installation & Setup

### Prerequisites (needed)
- Python 3.12 or higher
- Git
- Miniconda or Anaconda (recommended)

### Local Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/JosephMcLean118/logpose_project.git
   cd logpose_project/logpose_project
   ```

2. **Create and activate virtual environment**
   
   Using Conda (recommended):
   ```bash
   conda create -n logpose python=3.12.13
   conda activate logpose
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run database migrations**
   ```bash
   python manage.py migrate
   ```

5. **Create a superuser account**
   ```bash
   python manage.py createsuperuser
   ```
   Follow the prompts to create your admin account.

6. **Populate the database with sample data**
   ```bash
   python populate_logpose.py
   ```
   This will create:
   - 10 genres
   - 30 games with cover images
   - 5 test users
   - 10 sample reviews

7. **Run the development server**
   ```bash
   python manage.py runserver
   ```

8. **Access the application**
   - Main Site: http://127.0.0.1:8000/
   - Admin Panel: http://127.0.0.1:8000/admin/
   - Reviews Page: http://127.0.0.1:8000/reviews/
   - individual Review Page: http://127.0.0.1:8000/reviews/1/
   - Create a Review: http://127.0.0.1:8000/reviews/create/
   - Profile Page (Example User: Dennis): http://127.0.0.1:8000/user/dennis/
   - Edit Profile: http://127.0.0.1:8000/edit/
   - Login: http://127.0.0.1:8000/login/
   - Register: http://127.0.0.1:8000/register/

## 🌐 Deployment

The application is deployed on PythonAnywhere at:
**[https://2967122j.pythonanywhere.com]**

## Testing

The unit tests for the application can be run by running the follwing command inside /logpose_project
```bash
python manage.py test
```

## 📚 External Sources & Acknowledgments

This project makes use of the following external resources:

### Libraries & Frameworks
- **Bootstrap 5.3.3** - Responsive CSS framework — https://getbootstrap.com
- **Bootstrap Icons** - Icon library — https://icons.getbootstrap.com
- **Pillow 12.1.1** - Python image processing library — https://python-pillow.org

### Documentation & Learning Resources
- **Django Documentation** - https://docs.djangoproject.com/
- **Bootstrap Documentation** - https://getbootstrap.com/docs/

## 👨‍💻 Team Members and Github Usernames

- **Ali** - roonilaa
- **Joseph** - JosephMcLean118
- **Enoch** - EnochJ25
- **Gabriels** - GVillanuevaH05
- **Kai** - JokePanda


