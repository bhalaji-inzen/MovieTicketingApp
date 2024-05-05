# MovieTicketingApp

This app helps in theatre owners manage information about their theatres and shows(movies) and users book ticket for movies.

The Functionalities of the application includes creating, editing & deleting theaters and shows for admin users and booking tickets for the show for regular users.

It is a multi user application that has roles for the user & admin.

This app has token based authentication system and role based access control.

The features implemented in this project are
- User Login / Registration using flask security's token based authentication
- Theatre and show management (only for admin using RBAC)
- Book tickets for a show (User)
- Search for shows/theatres (User)
- Backend Jobs
    1. Daily reminders to users (via email) (Timed Jobs)
    2. Monthly reports to users (via email) (Timed Jobs)
    3. Generate reports for theatres (only for admin) (User Triggered Jobs)

Tech Used:

- Flask
- Flask-Security
- Flask-Caching
- Flask-SQLAlchemy
- Redis
- Celery
- Vue2 for FrontEnd
- smtplib
- sqlite for Database
- Bootstrap


### Environment Setup

```sh
python3 -m venv <environment-name>
```

### Install requirements 

```sh 
pip install -r requirements.txt
```

### Run app

```sh
python3 main.py
```

### Start Redis Server in another shell

```sh
redis-server
```

### Run Celery Worker

```sh
celery -A main.celery worker -l info
```

### Run Celery beat Scheduler for scheduling tasks

```sh
celery -A main.celery beat --max-interval 1 -l info
```