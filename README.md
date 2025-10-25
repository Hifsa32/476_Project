Unfiltered

A Django web app where users can share real stories, view posts, and report harmful or misleading content.

Features

User authentication (signup, login, logout)

Post creation and display on home feed

User profiles with display name and bio

Report form for inappropriate or false posts

Clean and responsive interface

Installation
git clone https://github.com/Hifsa32/476_Project.git
cd 476_Project
python -m venv .venv
source .venv/bin/activate  
pip install -r requirements.txt
python manage.py migrate
python manage.py loaddata fixtures.json

Usage
python manage.py runserver

Open http://127.0.0.1:8000
in your browser.

Demo Login:

Username: momo

Password: winnerss

You should be able to Sign up/log in, view posts, create new posts, report posts, access your profile and update your settings.
