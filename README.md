# Masoc

Masoc (short for **Make** + **Social**) is a social media web app built with Python and Django. I'm building it to learn web development.

## Features

- Sign up, log in, and log out
- Create posts
- Follow-based feed that shows your own posts plus posts from people you follow
- User profile pages with a bio (`/accounts/u/<username>/`)
- Follow / unfollow button

## Tech Stack

- Python
- Django
- SQLite (Django's default database)

## Getting Started

### 1. Clone the repository

```powershell
git clone https://github.com/mdmohibbulislam/Masoc.git
cd Masoc
```

### 2. Create and activate a virtual environment

```powershell
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies

```powershell
pip install -r requirements.txt
```

### 4. Set up the database

```powershell
python manage.py migrate
```

### 5. Run the development server

```powershell
python manage.py runserver
```

Then open http://127.0.0.1:8000/ in your browser.

## Roadmap

- [ ] Show a user's posts on their profile page
- [ ] More features coming soon

## Author

Made by [Mohib](https://github.com/mdmohibbulislam).
